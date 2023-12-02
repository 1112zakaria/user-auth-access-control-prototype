import unittest
from datetime import datetime, time
from unittest import mock

from problem1d import (AuthorizedTechnicalSupport, Client,
                           ComplianceOfficer, DefaultRole, FinancialAdvisor,
                           FinancialPlanner, InvestmentAnalyst, PremiumClient,
                           TechnicalSupport, Teller, get_role_from_str, Resource,
                           Access)


class TestAccessControl(unittest.TestCase):
    def setUp(self):
        self.default_role = DefaultRole()
        self.client_role = Client()
        self.premium_client_role = PremiumClient()
        self.financial_planner_role = FinancialPlanner()
        self.financial_advisor_role = FinancialAdvisor()
        self.investment_analyst_role = InvestmentAnalyst()
        self.technical_support_role = TechnicalSupport()
        self.authorized_technical_support_role = AuthorizedTechnicalSupport()
        self.teller_role = Teller()
        self.compliance_officer_role = ComplianceOfficer()

    def test_default_role_name(self):
        self.assertEqual(self.default_role.get_role_name(), "DefaultRole")

    def test_client_role_name(self):
        self.assertEqual(self.client_role.get_role_name(), "Client")

    def test_premium_client_role_name(self):
        self.assertEqual(self.premium_client_role.get_role_name(), "PremiumClient")

    def test_financial_planner_role_name(self):
        self.assertEqual(self.financial_planner_role.get_role_name(), "FinancialPlanner")

    def test_financial_advisor_role_name(self):
        self.assertEqual(self.financial_advisor_role.get_role_name(), "FinancialAdvisor")

    def test_investment_analyst_role_name(self):
        self.assertEqual(self.investment_analyst_role.get_role_name(), "InvestmentAnalyst")

    def test_technical_support_role_name(self):
        self.assertEqual(self.technical_support_role.get_role_name(), "TechnicalSupport")

    def test_authorized_technical_support_role_name(self):
        self.assertEqual(
            self.authorized_technical_support_role.get_role_name(), "AuthorizedTechnicalSupport"
        )

    def test_teller_role_name(self):
        self.assertEqual(self.teller_role.get_role_name(), "Teller")

    def test_compliance_officer_role_name(self):
        self.assertEqual(self.compliance_officer_role.get_role_name(), "ComplianceOfficer")

    def test_default_role_permissions(self):
        expected_permissions = {
            Resource.ACCOUNT_BALANCE: Access.NO,
            Resource.INVESTMENT_PORTFOLIO: Access.NO,
            Resource.FINANCIAL_ADVISOR_CONTACT_DETAILS: Access.NO,
            # Add other resources and their expected access values
        }
        expected_permissions = dict()
        self.assertEqual(self.default_role.get_permissions(), expected_permissions)

    # Write similar test methods for other roles

    @mock.patch("problem1d.datetime")
    def test_teller_role_permissions_during_working_hours(self, mock_datetime):
        mock_datetime.utcnow.return_value.time.return_value = time(10, 0)
        expected_permissions = {
            Resource.TELLER_SYSTEM_ACCESS: Access.VIEW,
            # Add other resources and their expected access values during working hours
        }
        self.assertEqual(self.teller_role.get_permissions(), expected_permissions)

    @mock.patch("problem1d.datetime")
    def test_teller_role_permissions_outside_working_hours(self, mock_datetime):
        mock_datetime.utcnow.return_value.time.return_value = time(18, 0)
        expected_permissions = {
            Resource.TELLER_SYSTEM_ACCESS: Access.NO,
            # Add other resources and their expected access values outside working hours
        }
        self.assertEqual(self.teller_role.get_permissions(), expected_permissions)

    def test_get_role_from_str(self):
        self.assertEqual(get_role_from_str("DefaultRole"), DefaultRole)
        self.assertEqual(get_role_from_str("Client"), Client)
        self.assertEqual(get_role_from_str("PremiumClient"), PremiumClient)
        # Add other role string tests

if __name__ == "__main__":
    unittest.main()
