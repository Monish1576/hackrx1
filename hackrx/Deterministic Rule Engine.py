class RuleEngine:
    RULE_TEMPLATES = {
        "distance_limit": lambda p: f"distance <= 150" if 'distance' in p else None,
        "waiting_period": lambda p: f"policy_age >= 24" if 'procedure' in p and 'orthopedic' in p[
            'procedure'] else None,
        "coverage_scope": lambda p: "location in India" if 'location' in p else None
    }

    def execute(self, params, clauses):
        decision = "approved"
        amount = None
        justification = []

        for rule_name, rule_func in self.RULE_TEMPLATES.items():
            rule_condition = rule_func(params)
            if rule_condition:
                # Find matching clause
                for clause in clauses:
                    if rule_name in clause['id']:
                        justification.append({
                            "clause_id": clause['id'],
                            "text": clause['text'][:50] + "...",
                            "rule": rule_condition
                        })
                        # Apply financial logic
                        if 'distance' in params and rule_name == "distance_limit":
                            amount = min(150, int(params['distance'])) * 100  # ₹100/km
                        break

        return {
            "decision": decision,
            "amount": amount,
            "justification": justification
        }