"""
Configuración del dashboard: caching y estado de servicios
"""

dashboard_services = ["ec2", "sg", "kp"]

summary_fallback = {
    "ec2": ("N/A", "N/A"),
    "sg": "N/A",
    "kp": "N/A"
}

dashboard_dirty = {
    "ec2": {
        "needs_update": True,
        "last_summary": None
    },
    "sg": {
        "needs_update": True,
        "last_summary": None,
    },
    "kp": {
        "needs_update": True,
        "last_summary": None
    }
}