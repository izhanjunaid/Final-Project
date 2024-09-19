Snake Game CRUD Application

Project Overview
This project is a Snake Game CRUD (Create, Read, Update, Delete) application developed as part of my final project for [Course Name]. The application is built using Flask and Redis, containerized with Docker, and deployed on Azure Kubernetes Service (AKS) using Terraform and Helm. The project also includes a CI/CD pipeline implemented with Jenkins.

Technologies Used
- Python (Flask)
- Redis
- Docker
- Kubernetes
- Terraform
- Helm
- Jenkins
- Azure (AKS and ACR)

Project Structure
snake-game-crud/
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── main.tf
├── Jenkinsfile
├── helm/
│   └── snake-game/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
│           ├── deployment.yaml
│           └── service.yaml
└── README.txt

Setup and Deployment
1. Clone this repository
2. Install required tools: Azure CLI, Terraform, Helm, Docker, kubectl
3. Set up Azure resources using Terraform:
   terraform init
   terraform apply
4. Build and push Docker image:
   az acr login --name snakegameacr
   docker build -t snakegameacr.azurecr.io/snake-game:latest .
   docker push snakegameacr.azurecr.io/snake-game:latest
5. Deploy with Helm:
   helm install snake-game ./helm/snake-game

API Endpoints
- POST /game: Start a new game
- GET /game/<game_id>: Get the current game state
- PUT /game/<game_id>: Update the game state
- DELETE /game/<game_id>: End a game

CI/CD Pipeline
The Jenkinsfile in this repository defines the CI/CD pipeline for building, testing, and deploying the application.

Challenges Faced
During the development of this project, I faced several challenges:
1. Configuring Terraform to set up the AKS cluster correctly
2. Creating a Helm chart that properly deploys the application
3. Setting up the Jenkins pipeline to automate the deployment process

Lessons Learned
This project taught me a lot about cloud deployment, containerization, and CI/CD processes. I gained hands-on experience with technologies like Docker, Kubernetes, and Terraform, which I believe will be valuable in my future career.

Future Improvements
If I had more time, I would like to:
1. Add a front-end interface for the game
2. Implement user authentication
3. Add more game features like power-ups or obstacles
4. Improve the test coverage of the application

Conclusion
This project has been a great learning experience, allowing me to apply classroom knowledge to a real-world application. It has strengthened my understanding of modern software development practices and cloud technologies.
EOL
