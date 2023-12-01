from enum import Enum, auto
from datetime import datetime, time
import json

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
    FINANCIAL_PLANNER_CONTACT_DETAILS   = 9
    INVESTMENT_ANALYST_CONTACT_DETAILS  = 4
    MONEY_MARKET_INSTRUMENTS            = 5
    PRIVATE_CONSUMER_INSTRUMENTS        = 6
    DERIVATIVES_TRADING                 = 7
    INTEREST_INSTRUMENTS                = 8
    CLIENT_INFORMATION                  = 10
    TELLER_SYSTEM_ACCESS                = 11


class Access(Enum):
    NO          = 0,
    VIEW        = 1,
    MODIFY      = 2,

# FIXME: use inheritance?
# Assume no access if not defined
class DefaultRole():
    def __init__(self):
        self.permissions: dict[Resource] = {}
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
    
    def get_role_name(self) -> str:
        return type(self).__name__
    
    def __str__(self) -> str:
        return self.get_role_name()
    
    def get_json_permissions(self):
        json_dict = {}
        for resource in self.permissions:
            json_dict[resource.name] = self.permissions[resource].name # access type, idk how to get typehint for this
        return json.dumps(json_dict)
    

class Client(DefaultRole):
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

class FinvestEmployee(DefaultRole):

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

class TechnicalSupport(DefaultRole):
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

class Teller(DefaultRole):
    def __init__(self):
        super().__init__()

    def init_permissions(self):
        super().init_permissions()
    
    def get_permissions(self):
        if _is_time_between(time(9,0), time(17, 0)):
            self.permissions[Resource.TELLER_SYSTEM_ACCESS] = Access.VIEW
        else:
            self.permissions[Resource.TELLER_SYSTEM_ACCESS] = Access.NO

class ComplianceOfficer(DefaultRole):
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


ROLE_LIST: 'list[DefaultRole]' = [
    DefaultRole,
    Client,
    PremiumClient,
    FinancialPlanner,
    FinancialAdvisor,
    InvestmentAnalyst,
    TechnicalSupport,
    AuthorizedTechnicalSupport,
    Teller
]

def get_role_from_str(role_str: str) -> DefaultRole:
    role_dict = {}

    for role in ROLE_LIST:
        role_dict[role.__name__] = role
    
    return role_dict.get(role_str, DefaultRole)

if __name__ == "__main__":
    r = DefaultRole()
    c = Client()
    p = PremiumClient()
    print(r.permissions)
    print(c.permissions)
    print(p.permissions)

