return {

	["folke/which-key.nvim"] = {
		disable = false,
	},
	["goolord/alpha-nvim"] = {
		disable = false,
	},
	["neovim/nvim-lspconfig"] = {
		config = function()
			require "plugins.configs.lspconfig"
			require "custom.plugins.lspconfig"
		end,
	},

	["nvim-treesitter/nvim-treesitter"] = {
		override_options = require "custom.plugins.treesitter",
	},

	["jose-elias-alvarez/null-ls.nvim"] = {
		requires = { "nvim-lua/plenary.nvim" },
		config = function()
			require "custom.plugins.nullls"
		end,
	},

	["lervag/vimtex"] = {},

	["max397574/better-escape.nvim"] = {
		config = function()
			require("better_escape").setup {
				mapping = { "jk", "kj", "jj", "kk" },
			}
		end,
	},

	["andweeb/presence.nvim"] = {},

    ["anuvyklack/pretty-fold.nvim"] = {
        config = function ()
            require('pretty-fold').setup()
        end
    }
}
