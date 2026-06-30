from app.events.event import Event


class EventEngine:

    def generate(self, matched_rules):

        events = []

        for rule in matched_rules:

            events.append(
                Event(
                    title=rule.name,
                    severity=rule.severity,
                    description=rule.description,
                )
            )

        return events