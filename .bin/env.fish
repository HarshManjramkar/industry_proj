if not contains "$HOME/Desktop/industry_proj/.bin" $PATH
    # Prepending path in case a system-installed binary needs to be overridden
    set -x PATH "$HOME/Desktop/industry_proj/.bin" $PATH
end
