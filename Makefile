.PHONY: help install doctor list-skills list-collections list-packs list-catalog \
	validate validate-backlog test build build-claude build-codex build-cursor build-copilot \
	catalog catalog-build backlog-generate backlog-promote-waves install-pack install-all check clean-dist

SKILLCTL := ./tools/skillctl
PYTHON ?= python3
export PYTHONPATH := tools$(if $(PYTHONPATH),:$(PYTHONPATH),)

help: ## Show available targets
	@awk 'BEGIN {FS = ":.*##"; printf "Usage: make [target]\n\nTargets:\n"} /^[a-zA-Z0-9_.-]+:.*##/ {printf "  %-18s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install skillctl locally (editable)
	$(PYTHON) -m pip install -e .

doctor: ## Check repository layout and Python version
	$(SKILLCTL) doctor

list-skills: ## List active skill IDs only
	$(SKILLCTL) list --skills

list-catalog: ## List all active skills with summaries (+ dist/catalog paths)
	@if [ -f dist/catalog/active-skills.md ]; then \
	  skills=$$(grep -c '^## ' dist/catalog/active-skills.md); \
	  echo "Catalog reports ($$skills active skills):"; \
	  echo "  dist/catalog/active-skills.md   human-readable (domain, modes, summary)"; \
	  echo "  dist/catalog/skills.json        machine-readable"; \
	  echo "  dist/catalog/packs.md           skills grouped by pack"; \
	  echo "  dist/catalog/coverage-by-mode.md  planning vs coding"; \
	  echo ""; \
	else \
	  echo "dist/catalog/ not found. Run 'make build' or 'make catalog-build' first."; \
	  echo ""; \
	fi
	$(SKILLCTL) catalog

list-collections: ## List collection IDs
	$(SKILLCTL) list --collections

list-packs: ## List pack IDs
	$(SKILLCTL) list --packs

validate: ## Validate skills, collections, and packs
	$(SKILLCTL) validate --all

validate-backlog: ## Validate proposed skills in registry/skill-backlog.yaml
	$(SKILLCTL) backlog validate

test: ## Run unit tests
	$(PYTHON) -m unittest discover -s tests -v

build: build-all ## Alias for build-all

build-all: validate ## Build Claude, Codex, Cursor, Copilot, and catalog output
	$(SKILLCTL) build --target all

build-claude: validate ## Build dist/claude only
	$(SKILLCTL) build --target claude

build-codex: validate ## Build dist/codex only
	$(SKILLCTL) build --target codex

build-cursor: validate ## Build dist/cursor only
	$(SKILLCTL) build --target cursor

build-copilot: validate ## Build dist/copilot only
	$(SKILLCTL) build --target copilot

catalog: ## Print active skill catalog
	$(SKILLCTL) catalog

catalog-build: ## Build dist/catalog reports
	$(SKILLCTL) catalog build --include-backlog

backlog-generate: ## Generate registry/skill-backlog.yaml from taxonomy
	$(SKILLCTL) backlog generate --from registry/taxonomy.yaml --out registry/skill-backlog.yaml --merge

backlog-promote-waves: backlog-generate ## Promote all configured waves to draft skill folders
	$(SKILLCTL) backlog promote --all-waves

install-pack: build ## Install active skills from PACK into DEST (Cursor)
	@test -n "$(PACK)" || (echo "Usage: make install-pack PACK=java-backend-pack DEST=/path/to/project"; exit 1)
	@test -n "$(DEST)" || (echo "Usage: make install-pack PACK=java-backend-pack DEST=/path/to/project"; exit 1)
	$(SKILLCTL) install --pack $(PACK) --target cursor --dest $(DEST)

install-all: build ## Install all active skills into DEST (Cursor)
	@test -n "$(DEST)" || (echo "Usage: make install-all DEST=/path/to/project"; exit 1)
	cp -R dist/cursor/.cursor $(DEST)/.cursor

check: validate validate-backlog test build-all ## Run the same checks as CI
	git diff --exit-code dist/

clean-dist: ## Remove generated dist output
	rm -rf dist/claude dist/codex dist/cursor dist/copilot dist/catalog
