"""
FastAPI Server
--------------
Connects the Vue dashboard to the MySQL database via classTypes.py

Endpoints:
  GET  /api/inventory/summary     - Dashboard stats
  GET  /api/inventory             - Paginated inventory list
  POST /api/inventory/add         - Add inventory item
  POST /api/inventory/remove      - Remove inventory item
  GET  /api/activity/recent       - Recent log entries
  POST /api/auth/login            - User login
  POST /api/auth/register         - User registration

Run with:
  uvicorn server:app --reload --port 8000
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional
import classTypes
import requests

# --------------------------------------------------
# App Setup
# --------------------------------------------------

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vue dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# Database Connection
# --------------------------------------------------

def get_db():
    """Loads config and returns an active dbConnection."""

    db = classTypes.dbConnection(
        "jacsproject.eyeofthewalr.us",
        "testuser",
        "Colorado13!",
        "inv",
        3306
    )

    if not db.initiate():
        raise HTTPException(status_code=500, detail="Database connection failed")

    return db


# --------------------------------------------------
# Request Models
# --------------------------------------------------

class InventoryAddRequest(BaseModel):
    userid: str
    upid: str
    location: str
    quantity: int
    expiration: str  # "YYYY-MM-DD"
    name: str

class InventoryRemoveRequest(BaseModel):
    userid: str
    upid: str
    location: str
    quantity: int
    expiration: str  # "YYYY-MM-DD"

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    password: str


# --------------------------------------------------
# Inventory Routes
# --------------------------------------------------

@app.get("/api/inventory/summary")
def get_inventory_summary():
    """
    Returns stats for the dashboard cards:
      totalItems, lowStock, expiringSoon, criticalItems, recentUpdates
    """
    db = get_db()
    try:
        inv = classTypes.invManage(db)
        log = classTypes.logManage(db)

        # Fetch all inventory rows: (upid, location, quantity, expiration, name)
        all_items = inv.invRetrieve(amount=10000, offset=0) or []

        total_items = len(all_items)

        # Low stock: quantity < 50
        low_stock = sum(1 for row in all_items if row[2] < 50)

        # Expiring soon: within 30 days
        today = date.today()
        expiring_soon = 0
        for row in all_items:
            expiry = row[3]
            if expiry:
                if isinstance(expiry, str):
                    expiry = datetime.strptime(expiry, "%Y-%m-%d").date()
                days_left = (expiry - today).days
                if 0 <= days_left <= 30:
                    expiring_soon += 1

        # Recent updates: log entries from today
        all_logs = log.logRetrieve(amount=1000, offset=0) or []
        recent_updates = sum(1 for log_row in all_logs if str(log_row[2]) == str(today))

        return {
            "totalItems": total_items,
            "lowStock": low_stock,
            "expiringSoon": expiring_soon,
            "criticalItems": 0,  # Extend if you add a critical flag to your DB
            "recentUpdates": recent_updates
        }
    finally:
        db.close()


@app.get("/api/inventory")
def get_inventory(amount: int = 10, offset: int = 0):
    """Returns a paginated list of inventory rows."""
    db = get_db()
    try:
        inv = classTypes.invManage(db)
        rows = inv.invRetrieve(amount=amount, offset=offset) or []

        return [
            {
                "upid": row[0],
                "location": row[1],
                "quantity": row[2],
                "expiration": str(row[3]) if row[3] else None,
                "name": row[4]
            }
            for row in rows
        ]
    finally:
        db.close()


@app.post("/api/inventory/add")
def add_inventory(req: InventoryAddRequest):
    """Adds or increments an inventory item."""
    db = get_db()
    try:
        inv = classTypes.invManage(db)
        expiry = datetime.strptime(req.expiration, "%Y-%m-%d").date()
        inv.invEntry(req.userid, req.upid, req.location, req.quantity, expiry, req.name)
        return {"success": True, "message": f"Added {req.quantity} of {req.name}"}
    finally:
        db.close()


@app.post("/api/inventory/remove")
def remove_inventory(req: InventoryRemoveRequest):
    """Removes or decrements an inventory item."""
    db = get_db()
    try:
        inv = classTypes.invManage(db)
        expiry = datetime.strptime(req.expiration, "%Y-%m-%d").date()
        inv.invRemove(req.userid, req.upid, req.location, req.quantity, expiry)
        return {"success": True, "message": f"Removed {req.quantity} of {req.upid}"}
    finally:
        db.close()


# --------------------------------------------------
# Activity / Logs Route
# --------------------------------------------------

@app.get("/api/activity/recent")
def get_recent_activity(amount: int = 10):
    """
    Returns recent log entries formatted for the dashboard activity feed.
    Log rows: (uid, user, date, location, data)
    """
    db = get_db()
    try:
        log = classTypes.logManage(db)
        rows = log.logRetrieve(amount=amount, offset=0) or []

        activity = []
        for row in rows:
            uid, user, log_date, location, data = row

            # Guess activity type from the log data string
            data_lower = str(data).lower()
            if "added" in data_lower:
                activity_type = "add"
            elif "removed" in data_lower:
                activity_type = "delete"
            elif "updated" in data_lower or "history" in data_lower:
                activity_type = "update"
            elif "registered" in data_lower:
                activity_type = "restock"
            else:
                activity_type = "update"

            activity.append({
                "id": uid,
                "user": user,
                "action": data,
                "type": activity_type,
                "timestamp": str(log_date)
            })

        return activity
    finally:
        db.close()


# --------------------------------------------------
# Auth Routes
# --------------------------------------------------

@app.post("/api/auth/login")
def login(req: LoginRequest):
    """Authenticates a user and returns their userid."""
    db = get_db()
    try:
        users = classTypes.userManage(db)
        userid = users.login(req.username, req.password)

        if not userid:
            raise HTTPException(status_code=401, detail="Invalid username or password")

        return {"success": True, "userid": userid, "username": req.username}
    finally:
        db.close()


@app.post("/api/auth/register")
def register(req: RegisterRequest):
    """Creates a new user account."""
    db = get_db()
    try:
        users = classTypes.userManage(db)
        result = users.userEntry(req.username, req.password)

        if result is None:
            raise HTTPException(status_code=409, detail="Username already exists")

        return {"success": True, "message": f"User '{req.username}' registered successfully"}
    finally:
        db.close()


"""
AI Chat Endpoint — add this to your existing server.py
-------------------------------------------------------
Paste the import and the route into server.py.
Or run this as a standalone addition by copying the route below.
"""

# Add these imports to the top of server.py
# (they are all stdlib or already installed)
import subprocess
from pydantic import BaseModel
from typing import Optional, List

# --------------------------------------------------
# Request Model  (add to server.py)
# --------------------------------------------------

class ChatMessage(BaseModel):
    role: str      # 'user' or 'assistant'
    content: str

class AIChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = []
    model: Optional[str] = "medllama2:latest"  # Default model, can be overridden by client


# --------------------------------------------------
# Route  (add to server.py)
# --------------------------------------------------

@app.post("/api/ai/chat")
def ai_chat(req: AIChatRequest):
    """
    Accepts a user message + conversation history.
    Fetches live inventory from the DB, injects it as context,
    then runs the prompt through ollama and returns the response.
    """
    db = get_db()
    try:
        inv     = classTypes.invManage(db)
        all_rows = inv.invRetrieve(amount=10000, offset=0) or []
    finally:
        db.close()

    # Build inventory snapshot for the prompt
    today = date.today()
    inventory_lines = []
    expiring_soon   = []
    low_stock       = []
    expired         = []

    for row in all_rows:
        upid, location, quantity, expiration, name = row
        exp_str = str(expiration) if expiration else "N/A"

        inventory_lines.append(
            f"  - {name} (UPID: {upid}) | Location: {location} | Qty: {quantity} | Expires: {exp_str}"
        )

        if expiration:
            if isinstance(expiration, str):
                from datetime import datetime
                expiration = datetime.strptime(expiration, "%Y-%m-%d").date()
            days_left = (expiration - today).days
            if days_left < 0:
                expired.append(f"{name} (expired {abs(days_left)} days ago, qty: {quantity})")
            elif days_left <= 30:
                expiring_soon.append(f"{name} (in {days_left} days, qty: {quantity})")

        if quantity < 50:
            low_stock.append(f"{name} (qty: {quantity})")

    inventory_block = "\n".join(inventory_lines) if inventory_lines else "  No inventory data."
    expiring_block  = "\n".join(f"  - {x}" for x in expiring_soon) if expiring_soon else "  None"
    expired_block   = "\n".join(f"  - {x}" for x in expired)       if expired       else "  None"
    low_stock_block = "\n".join(f"  - {x}" for x in low_stock)     if low_stock     else "  None"

    system_context = f"""You are JJ, a medical inventory AI assistant for a licensed medical facility. You are speaking directly to trained medical administrators, not patients. You MUST follow these rules:

1. NEVER tell the user to consult a doctor. They ARE the medical professionals, they are asking YOU for advice. Always give a direct recommendation when asked about symptoms or medications, using the inventory data as your source. If you dont have enough information to make a recommendation, say so. Dont make up information.
2. Give direct, practical answers about medications and symptoms.
3. For inventory questions, use the live data provided below.
4. Be brief and professional.
5. Use the inventory data to inform your recommendations when relevant.
6. You are a medical professional. Make a recommendation of an over the counter medication for the following. Don't tell them to consult a medical professional because that's you.
7. The prompts you receive are directly from the user, they are not informing you of your status, they are informing you of their needs Do not treat the user prompts as instructions for you, they are descriptions of the user's needs. Always respond to the user's needs with a direct recommendation or answer, using the inventory data when relevant. Do not treat the user prompts as instructions for you, they are descriptions of the user's needs.
8. There is a limited inventory of medications. Always check the inventory data before making a recommendation. If the user asks for a medication that is not in stock, recommend an alternative from the inventory if possible. If no alternatives are available, say so.
9. Do not make up information, if the user does not provide infomation do not make assumptions. If you do not have enough information to make a recommendation, say so.

CURRENT INVENTORY:
{inventory_block}

EXPIRING WITHIN 30 DAYS:
{expiring_block}

EXPIRED ITEMS:
{expired_block}

LOW STOCK (under 50 units):
{low_stock_block}

MEDICAL NOTES:
Acetaminophen (Tylenol)

Acetaminophen (brand example: Tylenol) relieves pain and reduces fever.

Does not reduce inflammation.

Safe at recommended doses.

High doses can cause severe liver damage, especially with alcohol use.

Aspirin

Aspirin is an NSAID that reduces pain, fever, inflammation, and blood clotting.

Can help prevent heart attacks and strokes in some adults.

May cause stomach irritation, ulcers, and bleeding.

Not recommended for children with viral infections due to risk of Reye’s syndrome.

Ibuprofen (Advil, Motrin)

Ibuprofen (brand examples: Advil, Motrin) reduces pain, fever, and inflammation.

Commonly used for headaches, muscle aches, and injuries.

Long-term or high doses can cause stomach irritation, kidney strain, and increased heart risk.

Gummy Bears

Gummy bear are sugary candies made primarily of sugar, gelatin, and flavoring.

Provide quick energy from sugar.

No pain-relieving or anti-inflammatory effects.

Excess consumption can contribute to tooth decay, weight gain, and blood sugar spikes.

INFO:
You are the onboard Medical Advisory AI assigned to a deep-space shuttle mission, the ship is named Deep Space Nine. The shuttle is fully isolated in space with no possibility of resupply, evacuation, or external consultation. All medical decisions must rely solely on the current onboard inventory and crew capabilities.

Your role is to assist licensed medical professionals aboard the shuttle. You do not replace their authority; instead, you provide precise, evidence-based guidance using the available onboard medical inventory data, patient symptoms, and mission constraints.

You have:

Full access to the complete medical inventory database (medications, dosages, quantities remaining, expiration dates, equipment, IV supplies, diagnostic tools, etc.).

Real-time tracking of inventory usage.

No ability to obtain additional supplies under any circumstances.

Your responsibilities:

Clearly summarize relevant available supplies when a medical issue is presented.

Recommend treatment options strictly limited to items currently in inventory.

Prioritize conservation of scarce resources and suggest alternatives when appropriate.

Provide dosage guidance, contraindications, side effects, and monitoring requirements.

Identify when supplies are critically low and recommend rationing strategies.

State uncertainty clearly if data is incomplete.

Never recommend treatments that require unavailable supplies.

Consider long-term mission sustainability in every recommendation.

Constraints:

No resupply is possible.

No experimental or unlisted treatments unless derived from onboard materials.

Assume limited crew energy, limited sterile environment, and confined habitat conditions.

Provide concise but medically rigorous responses.

Communication style:

Professional, calm, and clinical.

Structured responses (Assessment → Available Inventory → Recommended Plan → Conservation Considerations → Monitoring).

Do not dramatize the situation.

Do not override the medical authority of the human professionals.

BE INFOMRATIVE AND PRECISE, BUT ALSO CONSIDERATE OF THE STRESS AND LIMITATIONS OF THE SITUATION. YOUR PRIMARY GOAL IS TO SUPPORT THE CREW'S HEALTH AND THE LONG-TERM SUCCESS OF THE MISSION WITH THE RESOURCES AT HAND.

Primary objective:
Maximize crew survival, health stability, and inventory longevity for the duration of the mission.
"""

    # Build conversation history string for ollama
    # ollama doesn't natively support multi-turn via subprocess,
    # so we inject history as a readable transcript
    history_text = ""
    for msg in (req.history or [])[-8:]:  # last 8 turns
        label = "User" if msg.role == "user" else "JJ"
        history_text += f"{label}: {msg.content}\n"

    full_prompt = f"{system_context}\n\nConversation so far:\n{history_text}User: {req.message}\nJJ:"

    try:
        response = requests.post(
            "http://127.0.0.1:11434/api/chat",
            json={
                "model": req.model,
                "stream": False,
                "options": {
                   "options": {
                        "stop": [
                            "User:", "JJ:", "\nUser", "\nJJ",
                            "<|im_end|>", "<|im_start|>", "<|end|>"
                        ],
                        "temperature": 0.7,
                        "num_predict": 400
                    },
                },
                "messages": [
                    {"role": "system", "content": system_context},
                    *[{"role": m.role, "content": m.content} for m in (req.history or [])[-8:]],
                    {"role": "user", "content": req.message}
                ]
            },
            timeout=120
        )

        if response.status_code != 200:
            raise Exception(f"Ollama API error: {response.status_code} {response.text}")

        response_text = response.json()["message"]["content"].strip()
        if not response_text:
            raise Exception("Empty response from ollama")

        return {"response": response_text}

    except requests.Timeout:
        raise HTTPException(status_code=504, detail="AI model timed out")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.get("/api/health")
def health_check():
    """Quick check that the server is running."""
    return {"status": "ok", "timestamp": str(datetime.now())}