PURPLE = \033[95m
CYAN = \033[96m
DARKCYAN = \033[36m
BLUE = \033[94m
GREEN = \033[92m
YELLOW = \033[93m
RED = \033[91m
BOLD = \033[1m
UNDERLINE = \033[4m
END = \033[0m

help:
	@echo "$(YELLOW)# ------------------- Makefile commands ------------------- #$(END)"
	@echo ""
	@echo "$(GREEN)## DEV$(END)"
	@printf "$(CYAN)%-20s$(END) %b \n" "install-dev:" "Installs development dependencies"
	@printf "$(CYAN)%-20s$(END) %b \n" "run-dev:" "Runs development Docker containers"
	@printf "$(CYAN)%-20s$(END) %b \n" "dev:" "Builds and runs the development environment"
	@echo ""

	@echo "$(RED)## PROD$(END)"
	@printf "$(CYAN)%-20s$(END) %b \n" "act:" "Runs GitHub actions workflows using 'act'"
	@printf "$(CYAN)%-20s$(END) %b \n" "install-prod:" "Installs production dependencies"
	@printf "$(CYAN)%-20s$(END) %b \n" "zip:" "Creates a zip archive for production deployment"
	@echo ""

	@echo "$(BLUE)## TERRAFORM$(END)"
	@printf "$(CYAN)%-20s$(END) %b \n" "tf-init:" "Initializes Terraform in the 'terraform' directory"
	@printf "$(CYAN)%-20s$(END) %b \n" "tf-plan:" "Runs Terraform plan in the 'terraform' directory"
	@printf "$(CYAN)%-20s$(END) %b \n" "tf-apply:" "Applies Terraform changes in the 'terraform' directory"
	@printf "$(CYAN)%-20s$(END) %b \n" "tf-apply-dev:" "Applies Terraform changes with dev environment specifics"
	@echo ""


###########################################################
# DEV

install-dev:
	pip install -r requirements.dev.txt
run-dev:
	docker-compose --file docker-compose.dev.yaml up --force-recreate --build -d
	docker exec -it consultant_api bash
dev:
	docker-compose --file docker-compose.dev.yaml up --force-recreate --build
	docker exec -it consultant_api python main.py
bigbang:
	docker-compose --file docker-compose.dev.yaml up --force-recreate --build -d
	docker exec -d consultant_api python main.py

###########################################################
# PROD

act:
	act --container-architecture linux/amd64 --secret-file .secrets --var-file .vars
install-prod:
	pip install -t ./deps -r requirements.txt
zip:
	cd deps && zip ../lambda_function.zip -r .
	cd consultant && zip ../lambda_function.zip -u ./*


###########################################################
# TERRAFORM
tf-init:
	cd terraform && $(MAKE) init
tf-plan:
	cd terraform && $(MAKE) plan
tf-apply:
	cd terraform && $(MAKE) apply
tf-apply-dev:
	cd terraform && $(MAKE) apply-dev