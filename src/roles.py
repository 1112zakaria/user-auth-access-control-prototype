from enum import Enum

# Problem 1 Access Control

class Roles(Enum):
    CLIENT              = 1,
    PREMIUM_CLIENT      = 2,
    EMPLOYEE            = 3,
    ELEVATED_EMPLOYEE   = 4,
    FINANCIAL_PLANNER   = 5,
    INVESTMENT_ANALYST  = 6,
    FINANCIAL_ADVISOR   = 7,


