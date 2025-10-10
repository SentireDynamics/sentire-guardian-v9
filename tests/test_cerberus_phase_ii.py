#!/usr/bin/env python3
"""
Test de Cerberus Phase II - Validation des Actions Souveraines
"""
import pytest
from core.verbe_pur import Action
from guardian.cerberus import Cerberus
from core.exceptions import InvalidActionError


def test_cerberus_allows_sovereign_actions():
    """Test que Cerberus accepte les nouvelles actions souveraines."""
    cerberus = Cerberus()
    
    # Actions souveraines Phase II
    sovereign_actions = [
        Action(id="ISOLATE_PROCESS", description="Isolate process", parameters={"pid": 1234}),
        Action(id="EXCOMMUNICATE_PROCESS", description="Kill process", parameters={"pid": 1234}),
        Action(id="LOWER_RIVAL_PRIORITY", description="Lower priority", parameters={"pid": 1234}),
    ]
    
    # Actions classiques
    classic_actions = [
        Action(id="SHOW_MESSAGE", description="Show message", parameters={"title": "Test"}),
        Action(id="LOG_ONLY", description="Log only", parameters={}),
    ]
    
    # Toutes les actions doivent être acceptées
    all_actions = sovereign_actions + classic_actions
    
    for action in all_actions:
        assert cerberus.validate_action(action) == True
        print(f"✅ Action '{action.id}' acceptée par Cerberus")


def test_cerberus_rejects_invalid_actions():
    """Test que Cerberus rejette les actions non autorisées."""
    cerberus = Cerberus()
    
    # Actions non autorisées
    invalid_actions = [
        Action(id="DANGEROUS_ACTION", description="Dangerous", parameters={}),
        Action(id="UNKNOWN_ACTION", description="Unknown", parameters={}),
        Action(id="MALICIOUS_ACTION", description="Malicious", parameters={}),
    ]
    
    for action in invalid_actions:
        with pytest.raises(InvalidActionError):
            cerberus.validate_action(action)
        print(f"✅ Action '{action.id}' correctement rejetée par Cerberus")


if __name__ == "__main__":
    test_cerberus_allows_sovereign_actions()
    test_cerberus_rejects_invalid_actions()
    print("🎊 Tous les tests Cerberus Phase II réussis !")
