## DO NOT EDIT!
# This file was provisioned by Terraform
# File origin: https://github.com/Arrow-air/tf-github/tree/main/src/templates/all/.make/markdown.mk

MARKDOWN_FILES ?= $(shell find . -type f -iname '*md' ! -iwholename "*./node_modules/*" ! -path "./build" ! -iwholename "*.terraform*" ! -iwholename "*.cargo/*" ! -iwholename "./target/*")
LINK_CHECKER_JSON ?= .link-checker.config.json

.help-markdown:
	@echo ""
	@echo "$(SMUL)$(BOLD)$(GREEN)Markdown$(SGR0)"
	@echo "  $(BOLD)md-test-links$(SGR0)   -- Run markdown-link-check on all markdown files to catch dead links."

md-test-links:
ifeq ("$(MARKDOWN_FILES)", "")
	@echo "$(YELLOW)No markdown files found, skipping link validation...$(SGR0)"
else
ifeq ("$(wildcard $(LINK_CHECKER_JSON))","")
	@echo "$(YELLOW)No $(LINK_CHECKER_JSON) found, creating...$(SGR0)"
	echo -e "{\n}\n" > $(LINK_CHECKER_JSON)
endif
	@echo "$(CYAN)Checking if all document links are valid...$(SGR0)"
	@docker run \
		--name=$(DOCKER_NAME)-$@ \
		--rm \
		--user `id -u`:`id -g` \
		-w "/usr/src/app" \
		-v "$(PWD):/usr/src/app" \
		-t ghcr.io/tcort/markdown-link-check:3.10 \
		-c $(LINK_CHECKER_JSON) $(MARKDOWN_FILES)
endif
