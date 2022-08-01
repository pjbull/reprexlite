import re

try:
    import mkdocs
    from mkdocs.plugins import BasePlugin
except ImportError:
    raise Exception(
        'mkdocs package missing. To use the reprexlite mkdocs plugin, install using `pip install "reprexlite[mkdocs]"`.'
    )

from .reprex import reprex_list


class ReprexlitePlugin(BasePlugin):
    config_scheme = (
        # plugin specific config
        (
            "scope",
            mkdocs.config.config_options.Choice(("block", "page"), default="block"),
        ),
        (
            "reprexlite_regex",
            mkdocs.config.config_options.Type(str, default="```reprexlite(?P<code>.*?)```"),
        ),
        ("raise_on_error", mkdocs.config.config_options.Type(bool, default=False)),
        # passed through to the reprexlite.reprex function:
        #  https://jayqi.github.io/reprexlite/stable/api-reference/reprex/
        ("venue", mkdocs.config.config_options.Type(str, default="gh")),
        ("session_info", mkdocs.config.config_options.Type(bool, default=False)),
        ("style", mkdocs.config.config_options.Type(bool, default=False)),
        ("comment", mkdocs.config.config_options.Type(str, default="#>")),
        ("old_results", mkdocs.config.config_options.Type(bool, default=False)),
        ("print_", mkdocs.config.config_options.Type(bool, default=False)),
        (
            "advertise",
            mkdocs.config.config_options.Type(bool, default=False),
        ),  # TODO: add to mkdocs-reprexlite to advertise at bottom of page?
    )

    def on_pre_build(self, config):
        self.regex = re.compile(self.config["reprexlite_regex"], re.MULTILINE | re.DOTALL)

    def on_page_markdown(self, markdown, **kwargs):
        reprexlite_blocks = [m for m in self.regex.finditer(markdown)]

        reprexes = reprex_list(
            [m.group("code") for m in reprexlite_blocks],
            advertise=False,
            venue=self.config["venue"],
            session_info=self.config["session_info"],
            style=self.config["style"],
            comment=self.config["comment"],
            old_results=self.config["old_results"],
            print_=self.config["print_"],
            shared_namespace=(self.config["scope"] == "page"),
        )

        new_markdown = ""
        block_start = 0

        for orig, rep in zip(reprexlite_blocks, reprexes):
            # add text between previous block and this block
            new_markdown += markdown[block_start : orig.start(0)]

            if self.config["raise_on_error"] and rep.code_block.raised:
                start_n = len(markdown[: orig.start(0)].split("\n"))
                end_n = len(markdown[: orig.end(0)].split("\n"))

                raise mkdocs.exceptions.PluginError(
                    "reprexlite block generated an error "
                    + "(to ignore, set `raise_on_error` to False in mkdocs.yml): "
                    + "\n"
                    + f"File: '{kwargs['page'].file.src_path}', block on lines {start_n}-{end_n}"
                    + "\n\n"
                    + str(rep)
                )

            # add the rendered reprex
            new_markdown += str(rep)

            # set the continuation to the end of the match
            block_start = orig.end(0)

        # copy rest of document
        new_markdown += markdown[block_start:]

        return new_markdown
