from aura_life import LifeService

def state_to_text(svc: LifeService) -> str:
    s = svc.get_status()
    humor = s["affect"]["mood"]
    energia = s["energy_level"]
    metas = s["goals"]["active_goals"] or [{"title": "-"}]
    meta = metas[0]["title"]
    atividades = s["recent_activities_count"]

    return (
        f"Seu estado interno agora: humor={humor}, energia={energia}, "
        f"atividades recentes={atividades}, meta ativa='{meta}'."
    )
    
def tick_amadeus(world, amadeus):
    world.tick()
    amadeus._scheduler.force_all_ticks()
    return amadeus.get_status()