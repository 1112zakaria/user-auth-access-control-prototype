from enum import Enum, auto
from datetime import datetime, time

READ_ACCESS = 1
WRITE_ACCESS = 2

class RoleEnum(Enum):
    CLIENT              = 1
    PREMIUM_CLIENT      = 2
    EMPLOYEE            = 3
    ELEVATED_EMPLOYEE   = 4
    FINANCIAL_PLANNER   = 5
    INVESTMENT_ANALYST  = 6
    FINANCIAL_ADVISOR   = 7

class Resource(Enum):
    ACCOUNT_BALANCE                     = 1
    INVESTMENT_PORTFOLIO                = 2
    FINANCIAL_ADVISOR_CONTACT_DETAILS   = 3
    FINANCIAL_PLANNER_CONTACT_DETAILS   = auto()
    INVESTMENT_ANALYST_CONTACT_DETAILS  = 4
    MONEY_MARKET_INSTRUMENTS            = 5
    PRIVATE_CONSUMER_INSTRUMENTS        = 6
    DERIVATIVES_TRADING                 = 7
    INTEREST_INSTRUMENTS                = 8
    CLIENT_INFORMATION                  = auto()
    TELLER_SYSTEM_ACCESS                = auto()



class Access(Enum):
    NO          = 0,
    VIEW        = 1,
    MODIFY      = 2,

# FIXME: use inheritance?
# Assume no access if not defined
class Role():
    def __init__(self):
        self.permissions = {}
        self.init_permissions()
    
    def init_permissions(self):
        # override this method
        # initializes access to all resources to no access
        for resource in Resource:
            self.set_resource_access(resource, Access.NO)
    
    def set_resource_access(self, resource: Resource, access: Access):
        current_access: Access = self.permissions.get(resource, Access.NO)
        if (current_access.value < access.value):
            self.permissions[resource] = access
    
    def get_permissions(self):
        return self.permissions

class Client(Role):
    def __init__(self):
        super().__init__()
    
    def init_permissions(self):
        super().init_permissions()

        resources = [Resource.ACCOUNT_BALANCE, Resource.INVESTMENT_PORTFOLIO, Resource.FINANCIAL_ADVISOR_CONTACT_DETAILS]
        for resource in resources:
            self.set_resource_access(resource, Access.VIEW)

class PremiumClient(Client):
    def __init__(self):
        super().__init__()
    
    def init_permissions(self):
        super().init_permissions()

        self.set_resource_access(Resource.INVESTMENT_PORTFOLIO, Access.MODIFY)
        resources = [Resource.FINANCIAL_PLANNER_CONTACT_DETAILS, Resource.INVESTMENT_ANALYST_CONTACT_DETAILS]
        for resource in resources:
            self.set_resource_access(resource, Access.VIEW)

class FinvestEmployee(Role):

    def __init__(self):
        super().__init__()
    
    def init_permissions(self):
        super().init_permissions()

        resources = [Resource.ACCOUNT_BALANCE, Resource.INVESTMENT_PORTFOLIO]
        for resource in resources:
            self.set_resource_access(resource, Access.VIEW)

class PortfolioModifierAndPrivateInstrumentViewer(FinvestEmployee):
    def __init__(self):
        super().__init__()
    
    def init_permissions(self):
        super().init_permissions()
        self.set_resource_access(Resource.INVESTMENT_PORTFOLIO, Access.MODIFY)
        self.set_resource_access(Resource.PRIVATE_CONSUMER_INSTRUMENTS, Access.VIEW)

class FinancialPlanner(PortfolioModifierAndPrivateInstrumentViewer):
    def __init__(self):
        super().__init__()
    
    def init_permissions(self):
        super().init_permissions()
        self.set_resource_access(Resource.MONEY_MARKET_INSTRUMENTS, Access.VIEW)

class FinancialAdvisor(PortfolioModifierAndPrivateInstrumentViewer):
    pass

class InvestmentAnalyst(PortfolioModifierAndPrivateInstrumentViewer):
    def __init__(self):
        super().__init__()
    
    def init_permissions(self):
        super().init_permissions()
        self.set_resource_access(Resource.MONEY_MARKET_INSTRUMENTS, Access.VIEW)
        self.set_resource_access(Resource.DERIVATIVES_TRADING, Access.VIEW)
        self.set_resource_access(Resource.INTEREST_INSTRUMENTS, Access.VIEW)

class TechnicalSupport(Role):
    def __init__(self):
        super().__init__()
    
    def init_permissions(self):
        super().init_permissions()
        self.set_resource_access(Resource.CLIENT_INFORMATION, Access.VIEW)

class AuthorizedTechnicalSupportBase1(Client):
    pass

class AuthorizedTechnicalSupportBase2(TechnicalSupport):
    pass

class AuthorizedTechnicalSupport(AuthorizedTechnicalSupportBase2):
    def __init__(self):
        super().__init__()
    
    def init_permissions(self):
        super().init_permissions()

class Teller(Role):
    def __init__(self):
        super().__init__()

    def init_permissions(self):
        super().init_permissions()
    
    def get_permissions(self):
        if _is_time_between(time(9,0), time(17, 0)):
            self.permissions[Resource.TELLER_SYSTEM_ACCESS] = Access.VIEW
        else:
            self.permissions[Resource.TELLER_SYSTEM_ACCESS] = Access.NO

class ComplianceOfficer(Role):
    def __init__(self):
        super().__init__()
    
    def init_permissions(self):
        super().init_permissions()
        self.set_resource_access(Resource.INVESTMENT_PORTFOLIO, Access.VIEW)


def _is_time_between(begin_time, end_time):
    check_time = datetime.utcnow().time()

    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else:
        return check_time >= begin_time or check_time <= end_time


        
    
    

# PERMISSIONS = {
#     RoleEnum.CLIENT: {
#         Resource.ACCOUNT_BALANCE: Access.VIEW,
#         Resource.INVESTMENT_PORTFOLIO: Access.VIEW,
#         Resource.FINANCIAL_ADVISOR_CONTACT_DETAILS: Access.VIEW,
#     },
#     RoleEnum.PREMIUM_CLIENT: {
#         Resource.INVESTMENT_PORTFOLIO: Access.MODIFY,
#         Resource.FINANCIAL_ADVISOR_CONTACT_DETAILS: Access.VIEW,
#         Resource.INVESTMENT_ANALYST_CONTACT_DETAILS: Access.NO,
#         Resource.MONEY_MARKET_INSTRUMENTS: Access.NO,
#         Resource.PRIVATE_CONSUMER_INSTRUMENTS: Access.NO,
#     },
#     RoleEnum.EMPLOYEE: {},
#     RoleEnum.ELEVATED_EMPLOYEE: {},
#     RoleEnum.FINANCIAL_PLANNER: {},
#     RoleEnum.INVESTMENT_ANALYST: {},
#     RoleEnum.FINANCIAL_ADVISOR: {}
# }

def get_teller_access():
    now = datetime.datetime.now()
    print(now)

def get_permissions(role: RoleEnum, resource: Resource) -> Access:
    return PERMISSIONS[role][resource]

if __name__ == "__main__":
    #print(PERMISSIONS[RoleEnum.CLIENT][Resource.PRIVATE_CONSUMER_INSTRUMENTS])
    r = Role()
    c = Client()
    p = PremiumClient()
    print(r.permissions)
    print(c.permissions)
    print(p.permissions)

