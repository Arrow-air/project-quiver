## DO NOT EDIT!
# This file was provisioned by Terraform
# File origin: https://github.com/Arrow-air/tf-github/tree/main/src/templates/all/.make/cspell.mk
CSPELL_PROJECT_WORDS ?= .cspell.project-words.txt

.help-cspell:
	@echo ""
	@echo "$(SMUL)$(BOLD)$(GREEN)CSpell$(SGR0)"
	@echo "  $(BOLD)cspell-test$(SGR0)      -- Run 'cspell --words-only --unique "**/**" -c .cspell.config.yaml'"
	@echo "                      to validate files are not containing any spelling errors."
	@echo "  $(BOLD)cspell-add-words$(SGR0) -- Run 'cspell --words-only --unique "**/**" -c .cspell.config.yaml | "
	@echo "                      sort --ignore-case >> .cspell.project-words.txt'"
	@echo "                      to add remaining words to the project's cspell ignore list"

cspell-test: docker-pull
ifeq ("$(wildcard $(CSPELL_PROJECT_WORDS))","")
	@echo "$(YELLOW)No $(CSPELL_PROJECT_WORDS) found, creating...$(SGR0)"
	touch $(CSPELL_PROJECT_WORDS)
endif
	@echo "$(CYAN)Checking for spelling errors...$(SGR0)"
	@$(call docker_run,cspell --words-only --unique "**/**" -c .cspell.config.yaml)

cspell-add-words: docker-pull
	@echo "$(CYAN)Adding words to the project's cspell word list...$(SGR0)"
	@$(call docker_run,sh -c 'cspell --words-only --unique "**/**" -c .cspell.config.yaml 2> /dev/null | sort -f >> .cspell.project-words.txt')
