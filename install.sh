#!/usr/bin/env bash

# Claude Config Installer
# Interactive terminal UI for installing commands, skills, agents, and hooks

set -e

# Colors and styles
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
DIM='\033[2m'
RESET='\033[0m'
CLEAR_LINE='\033[2K'
HIDE_CURSOR='\033[?25l'
SHOW_CURSOR='\033[?25h'

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Global variables
declare -a TABS=("commands" "skills" "agents" "hooks")
declare -A SELECTED_ITEMS
CURRENT_TAB=0
CURRENT_ROW=0
SCROLL_OFFSET=0
MAX_DISPLAY_ROWS=15
FOCUS="list" # list, cancel, ok

# Terminal state
ORIGINAL_STTY=$(stty -g)

# Cleanup function
cleanup() {
    echo -ne "${SHOW_CURSOR}"
    stty "$ORIGINAL_STTY"
    tput cnorm 2>/dev/null || true
}
trap cleanup EXIT INT TERM

# Get terminal dimensions
get_terminal_size() {
    TERM_ROWS=$(tput lines)
    TERM_COLS=$(tput cols)
}

# Read available items from a category directory
get_items() {
    local category=$1
    local items=()

    if [[ ! -d "$SCRIPT_DIR/$category" ]]; then
        echo ""
        return
    fi

    case "$category" in
        commands)
            # List .md files
            while IFS= read -r file; do
                [[ -n "$file" ]] && items+=("$(basename "$file" .md)")
            done < <(find "$SCRIPT_DIR/$category" -maxdepth 1 -name "*.md" -type f 2>/dev/null | sort)
            ;;
        skills|agents)
            # List directories
            while IFS= read -r dir; do
                [[ -n "$dir" ]] && items+=("$(basename "$dir")")
            done < <(find "$SCRIPT_DIR/$category" -maxdepth 1 -mindepth 1 -type d 2>/dev/null | sort)
            ;;
        hooks)
            # List all files and directories
            while IFS= read -r item; do
                [[ -n "$item" ]] && items+=("$(basename "$item")")
            done < <(find "$SCRIPT_DIR/$category" -maxdepth 1 -mindepth 1 2>/dev/null | sort)
            ;;
    esac

    printf '%s\n' "${items[@]}"
}

# Draw the UI
draw_ui() {
    local target_project=$1
    get_terminal_size

    # Clear screen and hide cursor
    clear
    echo -ne "${HIDE_CURSOR}"

    # Header
    echo -e "${BOLD}${CYAN}═══════════════════════════════════════════════════════════════${RESET}"
    echo -e "${BOLD}${CYAN}    Claude Config Installer${RESET}"
    echo -e "${BOLD}${CYAN}═══════════════════════════════════════════════════════════════${RESET}"
    echo ""
    echo -e "${DIM}Target: ${RESET}$target_project"
    echo ""

    # Draw tabs
    echo -n "  "
    for i in "${!TABS[@]}"; do
        local tab="${TABS[$i]}"
        if [[ $i -eq $CURRENT_TAB ]]; then
            echo -ne "${BOLD}${BLUE}[ ${tab^^} ]${RESET} "
        else
            echo -ne "${DIM}[ ${tab} ]${RESET} "
        fi
    done
    echo ""
    echo ""

    # Get items for current tab
    local current_category="${TABS[$CURRENT_TAB]}"
    readarray -t items < <(get_items "$current_category")

    # Display items
    if [[ ${#items[@]} -eq 0 ]]; then
        echo -e "${DIM}  No items available in this category${RESET}"
        echo ""
    else
        local display_end=$((SCROLL_OFFSET + MAX_DISPLAY_ROWS))
        [[ $display_end -gt ${#items[@]} ]] && display_end=${#items[@]}

        for i in $(seq $SCROLL_OFFSET $((display_end - 1))); do
            local item="${items[$i]}"
            local key="${current_category}:${item}"
            local checkbox="[ ]"
            [[ -n "${SELECTED_ITEMS[$key]}" ]] && checkbox="[✓]"

            if [[ $i -eq $CURRENT_ROW ]] && [[ "$FOCUS" == "list" ]]; then
                echo -e "  ${BOLD}${GREEN}→ ${checkbox} ${item}${RESET}"
            else
                echo -e "    ${checkbox} ${item}"
            fi
        done
        echo ""

        # Scroll indicator
        if [[ ${#items[@]} -gt $MAX_DISPLAY_ROWS ]]; then
            local showing_end=$display_end
            echo -e "${DIM}  Showing $((SCROLL_OFFSET + 1))-${showing_end} of ${#items[@]}${RESET}"
            echo ""
        fi
    fi

    # Spacing
    for ((i=0; i<3; i++)); do echo ""; done

    # Draw buttons
    echo -n "  "
    if [[ "$FOCUS" == "cancel" ]]; then
        echo -ne "${BOLD}${RED}[ Cancel ]${RESET}  "
    else
        echo -ne "${DIM}[ Cancel ]${RESET}  "
    fi

    if [[ "$FOCUS" == "ok" ]]; then
        echo -ne "${BOLD}${GREEN}[ OK ]${RESET}"
    else
        echo -ne "${DIM}[ OK ]${RESET}"
    fi
    echo ""
    echo ""

    # Help text
    echo -e "${DIM}  ↑/↓: Navigate  Space: Select  Tab: Switch tabs  Enter: Confirm  Esc: Cancel${RESET}"
}

# Handle keyboard input
handle_input() {
    local current_category="${TABS[$CURRENT_TAB]}"
    readarray -t items < <(get_items "$current_category")
    local item_count=${#items[@]}

    # Read a single character
    local key
    IFS= read -rsn1 key

    # Handle escape sequences
    if [[ $key == $'\x1b' ]]; then
        read -rsn2 -t 0.01 key
        case "$key" in
            '[A') # Up arrow
                if [[ "$FOCUS" == "list" ]]; then
                    if [[ $item_count -gt 0 ]]; then
                        ((CURRENT_ROW--)) || CURRENT_ROW=$((item_count - 1))
                        # Adjust scroll
                        if [[ $CURRENT_ROW -lt $SCROLL_OFFSET ]]; then
                            SCROLL_OFFSET=$CURRENT_ROW
                        fi
                    fi
                else
                    FOCUS="list"
                    [[ $item_count -eq 0 ]] && CURRENT_ROW=0 || CURRENT_ROW=$((item_count - 1))
                    SCROLL_OFFSET=$((item_count > MAX_DISPLAY_ROWS ? item_count - MAX_DISPLAY_ROWS : 0))
                fi
                ;;
            '[B') # Down arrow
                if [[ "$FOCUS" == "list" ]]; then
                    if [[ $item_count -gt 0 ]]; then
                        ((CURRENT_ROW++)) || CURRENT_ROW=0
                        if [[ $CURRENT_ROW -ge $item_count ]]; then
                            CURRENT_ROW=0
                            SCROLL_OFFSET=0
                            FOCUS="cancel"
                        else
                            # Adjust scroll
                            if [[ $CURRENT_ROW -ge $((SCROLL_OFFSET + MAX_DISPLAY_ROWS)) ]]; then
                                SCROLL_OFFSET=$((CURRENT_ROW - MAX_DISPLAY_ROWS + 1))
                            fi
                        fi
                    else
                        FOCUS="cancel"
                    fi
                elif [[ "$FOCUS" == "cancel" ]]; then
                    :
                elif [[ "$FOCUS" == "ok" ]]; then
                    :
                fi
                ;;
            '[D') # Left arrow
                if [[ "$FOCUS" == "ok" ]]; then
                    FOCUS="cancel"
                fi
                ;;
            '[C') # Right arrow
                if [[ "$FOCUS" == "cancel" ]]; then
                    FOCUS="ok"
                fi
                ;;
        esac
        return 0
    fi

    case "$key" in
        $'\t') # Tab
            ((CURRENT_TAB++)) || true
            [[ $CURRENT_TAB -ge ${#TABS[@]} ]] && CURRENT_TAB=0
            CURRENT_ROW=0
            SCROLL_OFFSET=0
            FOCUS="list"
            ;;
        ' ') # Space
            if [[ "$FOCUS" == "list" ]] && [[ $item_count -gt 0 ]]; then
                local item="${items[$CURRENT_ROW]}"
                local key="${current_category}:${item}"
                if [[ -n "${SELECTED_ITEMS[$key]}" ]]; then
                    unset SELECTED_ITEMS["$key"]
                else
                    SELECTED_ITEMS["$key"]=1
                fi
            fi
            ;;
        $'\n'|$'\r') # Enter
            if [[ "$FOCUS" == "cancel" ]]; then
                return 1
            elif [[ "$FOCUS" == "ok" ]]; then
                return 2
            elif [[ "$FOCUS" == "list" ]]; then
                FOCUS="ok"
            fi
            ;;
        'q'|'Q'|$'\x1b') # q or Escape
            return 1
            ;;
    esac

    return 0
}

# Install selected items
install_items() {
    local target_project=$1
    local target_claude_dir="$target_project/.claude"

    # Create .claude directory if it doesn't exist
    if [[ ! -d "$target_claude_dir" ]]; then
        echo -e "${YELLOW}Creating .claude directory...${RESET}"
        mkdir -p "$target_claude_dir"
    fi

    local installed_count=0

    for key in "${!SELECTED_ITEMS[@]}"; do
        IFS=':' read -r category item <<< "$key"
        local source_path="$SCRIPT_DIR/$category/$item"
        local target_dir="$target_claude_dir/$category"

        # Create category directory if needed
        mkdir -p "$target_dir"

        case "$category" in
            commands)
                local source_file="$source_path.md"
                local target_file="$target_dir/${item}.md"
                if [[ -f "$source_file" ]]; then
                    cp "$source_file" "$target_file"
                    echo -e "${GREEN}✓${RESET} Installed command: ${item}"
                    ((installed_count++))
                fi
                ;;
            skills|agents)
                local target_path="$target_dir/$item"
                if [[ -d "$source_path" ]]; then
                    cp -r "$source_path" "$target_path"
                    echo -e "${GREEN}✓${RESET} Installed $category: ${item}"
                    ((installed_count++))
                fi
                ;;
            hooks)
                local target_path="$target_dir/$item"
                if [[ -e "$source_path" ]]; then
                    cp -r "$source_path" "$target_path"
                    echo -e "${GREEN}✓${RESET} Installed hook: ${item}"

                    # If hook has a settings.json, merge it
                    if [[ -f "$source_path/settings.json" ]]; then
                        echo -e "${YELLOW}  Note: Hook configuration found in $item/settings.json${RESET}"
                        echo -e "${YELLOW}  You need to manually merge this into your .claude/settings.json${RESET}"
                    fi
                    ((installed_count++))
                fi
                ;;
        esac
    done

    echo ""
    echo -e "${BOLD}${GREEN}Installation complete!${RESET} Installed ${installed_count} item(s)."
}

# Main function
main() {
    local target_project=""

    # Parse arguments
    if [[ $# -eq 0 ]]; then
        echo -e "${BOLD}Enter target project path:${RESET}"
        read -r target_project
    else
        target_project="$1"
    fi

    # Validate target project
    if [[ ! -d "$target_project" ]]; then
        echo -e "${RED}Error: Target project directory does not exist: $target_project${RESET}"
        exit 1
    fi

    # Convert to absolute path
    target_project=$(cd "$target_project" && pwd)

    # Setup terminal
    stty -echo -icanon min 1 time 0

    # Main loop
    while true; do
        draw_ui "$target_project"

        if handle_input; then
            continue
        else
            local exit_code=$?
            if [[ $exit_code -eq 1 ]]; then
                # Cancelled
                echo -e "${YELLOW}Installation cancelled.${RESET}"
                exit 0
            elif [[ $exit_code -eq 2 ]]; then
                # OK pressed
                break
            fi
        fi
    done

    # Restore terminal and show cursor
    cleanup
    echo ""

    # Install selected items
    if [[ ${#SELECTED_ITEMS[@]} -eq 0 ]]; then
        echo -e "${YELLOW}No items selected. Nothing to install.${RESET}"
    else
        echo -e "${BOLD}Installing selected items...${RESET}"
        echo ""
        install_items "$target_project"
    fi
}

main "$@"
