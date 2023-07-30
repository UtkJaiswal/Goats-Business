# Goats Business


## Backend Setup

### Getting started with backend
-   Navigate to the backend directory: cd project
-   Create a virtual environment (optional but recommended): python -m venv venv
-   Activate the virtual environment:
    -   On Windows: venv\Scripts\activate
    -   On macOS and Linux: source venv/bin/activate
-   Install the required packages: pip install -r requirements.txt
-   Apply migrations: python manage.py migrate
-   Start the backend development server: python manage.py runserver
-   The backend API will be accessible at http://localhost:8000

### API endpoints

-   Users
    -   GET /api/users/: Get a list of all users.
    -   POST /api/users/: Create a new user.

-   Goats
    -   GET /api/goats/: Get a list of all goats.
    -   POST /api/goats/: Create a new goat.

-   Loads
    -   GET /api/loads/: Get a list of all loads.
    -   POST /api/loads/: Create a new load.

-   Seller Create Goat
    -   POST /api/seller-create-goat/: Create goats associated with a seller_id.

-   Agent Goat List
    -   GET /api/agent-goat-list/:agent_id/: Get a list of goats associated with a specific agent.

-   Seller Selling to Agent
    -   POST /api/seller-selling-to-agent/: Record the transaction when a seller sells goats to an agent.

-   Agent Merge Split
    -   PUT /api/agent-merge-split/:id/: Perform merge or split operation for agents.

-   Agent Selling to Buyer
    -   POST /api/agent-selling-to-buyer/: Record the transaction when an agent sells goats to a buyer.

-   Sales
    -   GET /api/sales/: Get a list of all sales.
    -   POST /api/sales/: Create a new sale.

-   Buyer Goat List
    -   GET /api/buyer-goat-list/:buyer_id/: Get a list of goats associated with a specific buyer.

** The Thunderclient file collection which includes all the endpoints created is added in the `project` directory **


## Frontend

### Getting Started


### Frontend Setup
-   Navigate to the frontend directory: cd client/goat-app
-   Install the required dependencies: npm install
-   Start the frontend development server: npm start
-   The frontend will be accessible at http://localhost:3000.