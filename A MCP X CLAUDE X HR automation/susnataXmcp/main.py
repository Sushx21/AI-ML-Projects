from mcp.server.fastmcp import FastMCP
from typing import List
import json, os

"""
CallLeaveManager MCP Server
===========================

This MCP (Model Context Protocol) server simulates an internal HR system for tracking: 
 
Concurrent Handling Time (CHT) per employee 
 
Leave balance and leave history 
  
Leave applications and revocations
The system supports:
- Retrieving employee summaries
- Applying and revoking leaves
- Fetching leave history
- Basic greeting resource for conversational use

All data is persisted locally in JSON format to retain state between restarts.

Author: Susnata
"""

# ===================================================
# EMPLOYEE DATA (Persistent)
# ===================================================

EMPLOYEE_FILE = "D:\\susnataXmcp\\employee_data.json"

if os.path.exists(EMPLOYEE_FILE):
    with open(EMPLOYEE_FILE, "r") as f:
        employee_data = json.load(f)
else:
    employee_data = {
        "EMP001": {"name": "Aarav Sen", "cht": 5.2, "leaves": {"balance": 20, "history": []}},
        "EMP002": {"name": "Priya Mehta", "cht": 5.5, "leaves": {"balance": 20, "history": []}},
        "EMP003": {"name": "Rohan Das", "cht": 6.1, "leaves": {"balance": 20, "history": []}},
        "EMP004": {"name": "Ishita Roy", "cht": 5.8, "leaves": {"balance": 20, "history": []}},
        "EMP005": {"name": "Kabir Khanna", "cht": 6.7, "leaves": {"balance": 20, "history": []}},
        "EMP006": {"name": "Neha Kapoor", "cht": 5.9, "leaves": {"balance": 20, "history": []}},
        "EMP007": {"name": "Arjun Patel", "cht": 6.3, "leaves": {"balance": 20, "history": []}},
        "EMP008": {"name": "Meera Sinha", "cht": 6.0, "leaves": {"balance": 20, "history": []}},
        "EMP009": {"name": "Dev Sharma", "cht": 5.6, "leaves": {"balance": 20, "history": []}},
        "EMP010": {"name": "Riya Nair", "cht": 6.4, "leaves": {"balance": 20, "history": []}},
        "EMP011": {"name": "Aditya Ghosh", "cht": 6.2, "leaves": {"balance": 20, "history": []}},
        "EMP012": {"name": "Sanjana Iyer", "cht": 5.7, "leaves": {"balance": 20, "history": []}},
        "EMP013": {"name": "Vikram Bhat", "cht": 6.5, "leaves": {"balance": 20, "history": []}},
        "EMP014": {"name": "Tanya Malhotra", "cht": 5.3, "leaves": {"balance": 20, "history": []}},
        "EMP015": {"name": "Karan Joshi", "cht": 6.6, "leaves": {"balance": 20, "history": []}},
        "EMP016": {"name": "Nisha Chatterjee", "cht": 5.4, "leaves": {"balance": 20, "history": []}},
        "EMP017": {"name": "Rahul Banerjee", "cht": 6.8, "leaves": {"balance": 20, "history": []}},
        "EMP018": {"name": "Aanya Desai", "cht": 5.1, "leaves": {"balance": 20, "history": []}},
        "EMP019": {"name": "Siddharth Rao", "cht": 6.9, "leaves": {"balance": 20, "history": []}},
        "EMP020": {"name": "Diya Mukherjee", "cht": 5.0, "leaves": {"balance": 20, "history": []}}
    }

    with open(EMPLOYEE_FILE, "w") as f:
        json.dump(employee_data, f, indent=4)


def save_employee_data():
    with open(EMPLOYEE_FILE, "w") as f:
        json.dump(employee_data, f, indent=4)


# ===================================================
# MCP SERVER INITIALIZATION
# ===================================================

mcp = FastMCP("SusnataAgentparameter")


# ===================================================
# TOOL 1: EMPLOYEE SUMMARY
# ===================================================
@mcp.tool()
def get_employee_summary(employee_id: str) -> str:
    """
    Return a concise summary of an employee's performance and leave details.
    Used by LLM tools to retrieve quick information about an employee.
    """
    emp = employee_data.get(employee_id)
    if not emp:
        return f"Employee ID {employee_id} not found."

    return (
        f"Employee: {emp['name']} ({employee_id})\n"
        f"Average CHT: {emp['cht']} minutes\n"
        f"Leave Balance: {emp['leaves']['balance']} days\n"
        f"Total Leaves Taken: {len(emp['leaves']['history'])}"
    )


# ===================================================
# TOOL 2: APPLY LEAVE
# ===================================================
@mcp.tool()
def apply_leave(employee_id: str, leave_dates: List[str]) -> str:
    """
    Apply for leave on the given dates and update persistent state.
    LLMs use this tool to simulate a leave request workflow.
    """
    emp = employee_data.get(employee_id)
    if not emp:
        return f"Employee ID {employee_id} not found."

    requested_days = len(leave_dates)
    balance = emp["leaves"]["balance"]

    if requested_days > balance:
        return f"Insufficient balance. Requested {requested_days}, available {balance}."

    emp["leaves"]["balance"] -= requested_days
    emp["leaves"]["history"].extend(leave_dates)
    save_employee_data()

    return (
        f"Leave applied for {requested_days} day(s): {', '.join(leave_dates)}.\n"
        f"Remaining Balance: {emp['leaves']['balance']} days."
    )


# ===================================================
# TOOL 3: REVOKE LEAVE
# ===================================================
@mcp.tool()
def revoke_leave(employee_id: str, leave_dates: List[str]) -> str:
    """
    Revoke one or more approved leave dates and restore the leave balance.
    Designed for LLM-driven leave management adjustments.
    """
    emp = employee_data.get(employee_id)
    if not emp:
        return f"Employee ID {employee_id} not found."

    revoked = [d for d in leave_dates if d in emp["leaves"]["history"]]
    if not revoked:
        return f"No matching leave dates found for {employee_id}."

    for d in revoked:
        emp["leaves"]["history"].remove(d)

    emp["leaves"]["balance"] += len(revoked)
    save_employee_data()

    return (
        f"Revoked leave(s): {', '.join(revoked)}.\n"
        f"Updated Balance: {emp['leaves']['balance']} days."
    )


# ===================================================
# TOOL 4: LEAVE HISTORY
# ===================================================
@mcp.tool()
def get_leave_history(employee_id: str) -> str:
    """
    Retrieve all historical leave records for an employee.
    Enables audit-style queries through conversational agents.
    """
    emp = employee_data.get(employee_id)
    if not emp:
        return f"Employee ID {employee_id} not found."

    history = emp["leaves"]["history"]
    if not history:
        return f"{emp['name']} ({employee_id}) has not taken any leave yet."

    return f"Leave history for {emp['name']} ({employee_id}): {', '.join(history)}"


# ===================================================
# RESOURCE: GREETING
# ===================================================
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """
    Generate a short personalized greeting message for an employee.
    Used by chat interfaces or HR dashboards.
    """
    return f"Hello {name}, how can I assist with your leave management today?"


# ===================================================
# ENTRY POINT
# ===================================================
if __name__ == "__main__":
    mcp.run()

