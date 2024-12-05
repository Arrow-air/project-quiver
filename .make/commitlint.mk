## DO NOT EDIT!
# This file was provisioned by Terraform
# File origin: https://github.com/Arrow-air/tf-github/tree/main/src/templates/all/.make/commitlint.mk

COMMITLINT_CHECK :=

.help-commitlint:
	@echo ""
	@echo "$(SMUL)$(BOLD)$(GREEN)Commitlint$(SGR0)"
	@echo "  $(BOLD)commitlint-test$(SGR0)  -- Run 'commitlint --edit $(COMMITLINT_CHECK)'"
	@echo "                      to validate commit messages are following the conventional commit standards."

commitlint-test: docker-pull
	@echo "$(CYAN)Checking for commit message errors...$(SGR0)"
	@$(call docker_run,commitlint --edit $(COMMITLINT_CHECK))
