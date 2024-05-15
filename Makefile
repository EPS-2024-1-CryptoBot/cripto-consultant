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
	@echo "$(GREEN)@ DEV$(END)"	
	@printf "$(CYAN)%-30b$(END) %b\n" "help:" "Shows this message."
	@printf "$(CYAN)%-30b$(END) %b\n" "install-dev:" "Install the dev dependencies."

install-dev:
	pip install -r requirements.dev.txt
run-dev:
	docker-compose --file docker-compose.dev.yaml up --force-recreate --build -d
	docker exec -it consultant_api bash
dev:
	docker-compose --file docker-compose.dev.yaml up --force-recreate --build -d
	docker exec -it consultant_api python main.py