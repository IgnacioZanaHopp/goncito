import random
from typing import Dict, List, Callable

class SocialAttribute:
    """
    Representa un atributo social (ej. amistad, respeto, miedo) con valores entre -1.0 y 1.0.
    """
    def __init__(self, name: str, default: float = 0.0):
        self.name = name
        self.values: Dict[str, float] = {}
        self.default = default

    def get(self, actor: str) -> float:
        return self.values.get(actor, self.default)

    def adjust(self, actor: str, delta: float) -> None:
        new_val = self.get(actor) + delta
        # Clamping entre -1 y 1
        self.values[actor] = max(-1.0, min(1.0, new_val))

class SocialMove:
    """
    Define un movimiento social con precondiciones y efectos sobre atributos.
    name: identificador del movimiento.
    precond: función(net, source, target) -> bool si puede ejecutarse.
    effect: función(net, source, target) que ajusta atributos.
    """
    def __init__(self,
                 name: str,
                 precond: Callable[['SocialNetwork', str, str], bool],
                 effect: Callable[['SocialNetwork', str, str], None]):
        self.name = name
        self.precond = precond
        self.effect = effect

class SocialNetwork:
    """
    Versión ampliada de CiF-CK: mantiene atributos sociales y decide movimientos basados en condiciones y probabilidades.
    """
    def __init__(self, npcs: List[str]):
        # Inicializa atributos sociales
        self.attributes: Dict[str, SocialAttribute] = {
            'amistad': SocialAttribute('amistad', 0.0),
            'respeto': SocialAttribute('respeto', 0.0),
            'miedo': SocialAttribute('miedo', 0.0)
        }
        self.moves: List[SocialMove] = []
        self.actors = set(npcs + ['Jugador'])
        self._build_moves()

    def _build_moves(self) -> None:
        # Ayudar: solo si amistad > 0.2
        def pre_help(net, src, tgt):
            return net.attributes['amistad'].get(tgt) > 0.2
        def eff_help(net, src, tgt):
            net.attributes['amistad'].adjust(tgt, 0.3)
            net.attributes['respeto'].adjust(tgt, 0.2)
        self.moves.append(SocialMove('ayudar', pre_help, eff_help))

        # Insulto: si amistad < 0.0
        def pre_insult(net, src, tgt):
            return net.attributes['amistad'].get(tgt) < 0.0
        def eff_insult(net, src, tgt):
            net.attributes['respeto'].adjust(tgt, -0.4)
            net.attributes['miedo'].adjust(tgt, 0.3)
        self.moves.append(SocialMove('insultar', pre_insult, eff_insult))

        # Chismear: siempre disponible
        def pre_gossip(net, src, tgt):
            return src != tgt
        def eff_gossip(net, src, tgt):
            net.attributes['respeto'].adjust(tgt, -0.1)
        self.moves.append(SocialMove('chismear', pre_gossip, eff_gossip))

        # Elogio: aumenta respeto
        def pre_praise(net, src, tgt):
            return True
        def eff_praise(net, src, tgt):
            net.attributes['respeto'].adjust(tgt, 0.3)
            net.attributes['amistad'].adjust(tgt, 0.1)
        self.moves.append(SocialMove('elogiar', pre_praise, eff_praise))

    def get_valid_moves(self, source: str, target: str) -> List[SocialMove]:
        # Retorna movimientos que cumplen precondiciones y actores válidos
        if source not in self.actors or target not in self.actors:
            return []
        return [m for m in self.moves if m.precond(self, source, target)]

    def decide_move(self, source: str, target: str) -> SocialMove:
        """
        Elige un movimiento válido de forma aleatoria ponderada.
        Se puede ampliar para ponderar según atributos.
        """
        valids = self.get_valid_moves(source, target)
        if not valids:
            return None
        # Opcional: ponderar por diferencia de atributo respeto-amistad
        weights = []
        for m in valids:
            # Ejemplo simple: igual probabilidad
            weights.append(1)
        return random.choices(valids, weights=weights, k=1)[0]

    def execute_move(self, move: SocialMove, source: str, target: str) -> None:
        """
        Aplica el efecto del movimiento y actualiza atributos.
        """
        if move:
            move.effect(self, source, target)

    def get_attribute(self, attr_name: str, actor: str) -> float:
        """
        Consulta el valor de un atributo para un actor.
        """
        attr = self.attributes.get(attr_name)
        return attr.get(actor) if attr else 0.0
