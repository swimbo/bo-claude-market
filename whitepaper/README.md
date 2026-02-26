# Whitepaper Plugin for Claude Code

Technical whitepaper authoring plugin that guides users through creating high-quality whitepapers with structured workflows, research, review, and PDF generation.

## Features

* Full lifecycle support: discovery, outline, research, draft, review, revise, finalize

* 6 whitepaper types: Pure Technical, Problem/Solution, Backgrounder, Thought Leadership, Market Research, Visionary

* Custom requirements mode: extract format rules from RFPs, style guides, or templates

* WebSearch-powered research for real citations and data

* Quality review against comprehensive checklist

* PDF generation via pandoc

* Author history for quick reuse

## Commands

| Command              | Description                       | Usage                                         |
| -------------------- | --------------------------------- | --------------------------------------------- |
| `/whitepaper:create` | Create a whitepaper from scratch  | `/whitepaper:create Cloud Migration Strategy` |
| `/whitepaper:custom` | Create from requirements document | `/whitepaper:custom ./rfp-requirements.pdf`   |
| `/whitepaper:review` | Review an existing draft          | `/whitepaper:review ./draft.md`               |
| `/whitepaper:revise` | Revise a draft based on feedback  | `/whitepaper:revise ./draft.md`               |

## Agents

| Agent                    | Triggers On                         | Purpose                                                           |
| ------------------------ | ----------------------------------- | ----------------------------------------------------------------- |
| `whitepaper-researcher`  | Research phase of creation/revision | Gathers citations, statistics, case studies via WebSearch         |
| `whitepaper-reviewer`    | Review phase                        | Evaluates drafts against quality checklist with scored categories |
| `requirements-extractor` | Custom mode                         | Parses requirement docs into structured profiles                  |

## Prerequisites

For PDF generation:

* [pandoc](https://pandoc.org/installing.html) (`brew install pandoc`)

* A LaTeX engine (`brew install --cask mactex-no-gui`) or weasyprint (`pip install weasyprint`)

## Installation

The plugin is installed at `~/.claude/plugins/whitepaper/`.

To verify it loads, restart Claude Code and check:

* `/whitepaper:create` appears in command list

* Mentioning "whitepaper" activates the authoring skill