from app.rules.rules import RULES


class RuleEngine:

    def evaluate(self, analytics):

        matched_rules = []

        for rule in RULES:

            if rule.condition(analytics):

                matched_rules.append(rule)

        return matched_rules