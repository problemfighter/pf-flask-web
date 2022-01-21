
class PWebFlaskUtil:

    @staticmethod
    def is_url_register(flask_app, url):
        if not url or url == "":
            return True
        for url_rule in flask_app.url_map.iter_rules():
            if url_rule.rule == url:
                return True
        return False
