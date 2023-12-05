# User Authentication and Access Control Prototype
Author: Zakaria Ismail

# Setup Instructions

## Install Dependencies

On the SEED Labs VM, install:

Flask
```
pip3 install flask
```

# Run Instructions

This system consists of a client and a server application.

Go to the `src` directory using:
```
cd src
```

Then, run the server in one window using:
```
python3 auth_server.py
```

Then, run the login client in another window using:
```
python3 login.py
```

To run the enroll client, run the following in another window:
```
python3 enroll.py
```
# Test Instructions

To run the tests, execute the following command:

```
python -m unittest discover src/tests
```


# Unit Tests added for Role Classes
This section describes the new unit tests that were added to verify the permissions of different user roles.

- `Client`: Tests verify basic account viewing capabilities without access to sensitive financial resources.
- `PremiumClient`: Checks for extended privileges over the `Client` role including access to investment portfolio.
- `FinancialPlanner`: Focuses on accessibility to relevant financial planning resources.
- `FinancialAdvisor`: Evaluates access to advisee accounts and investment portfolios during specified working hours.
- `InvestmentAnalyst`: Assesses the ability to view investment portfolios but restricts client and advisor contact details.
- `TechnicalSupport`: Confirms no access to sensitive account information while providing technical assistance.
- `AuthorizedTechnicalSupport`: Similar to `TechnicalSupport`, but checks for specific scenarios where elevated permissions are granted.
- `ComplianceOfficer`: Tests for comprehensive access to uphold system compliance across financial operations.
- `Teller` (time-based): Tests are scenario-focused, ensuring tellers have access to the necessary resources only during their working hours to handle transactions.

These tests are essential to ensure that each role is only granted permissions that align with their responsibilities within the system. This is important to maintain security and privacy norms as per the access control policy.
