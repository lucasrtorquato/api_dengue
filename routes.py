from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import get_db
from models import FocoDengue
from schemas import FocoCreate

router = APIRouter()

TIPOS_VALIDOS = [
    "Água parada",
    "Terreno abandonado",
    "Lixo acumulado",
    "Piscina sem manutenção"
]


@router.post("/focos")
def criar_foco(
    foco: FocoCreate,
    db: Session = Depends(get_db)
):

    if foco.tipo not in TIPOS_VALIDOS:
        raise HTTPException(
            status_code=400,
            detail="Tipo inválido"
        )

    novo = FocoDengue(**foco.model_dump())

    db.add(novo)
    db.commit()
    db.refresh(novo)

    return novo


@router.get("/focos")
def listar_focos(
    db: Session = Depends(get_db)
):
    return db.query(FocoDengue).all()


@router.get("/focos/{id}")
def buscar_foco(
    id: int,
    db: Session = Depends(get_db)
):

    foco = db.query(FocoDengue)\
        .filter(FocoDengue.id == id)\
        .first()

    if not foco:
        raise HTTPException(
            status_code=404,
            detail="Foco não encontrado"
        )

    return foco


@router.delete("/focos/{id}")
def excluir_foco(
    id: int,
    db: Session = Depends(get_db)
):

    foco = db.query(FocoDengue)\
        .filter(FocoDengue.id == id)\
        .first()

    if not foco:
        raise HTTPException(
            status_code=404,
            detail="Foco não encontrado"
        )

    db.delete(foco)
    db.commit()

    return {"mensagem": "Excluído com sucesso"}


@router.put("/focos/{id}/resolver")
def marcar_resolvido(
    id: int,
    db: Session = Depends(get_db)
):

    foco = db.query(FocoDengue)\
        .filter(FocoDengue.id == id)\
        .first()

    if not foco:
        raise HTTPException(
            status_code=404,
            detail="Foco não encontrado"
        )

    foco.status = "Resolvido"

    db.commit()

    return {
        "mensagem": "Foco resolvido"
    }


@router.get("/dashboard")
def dashboard(
    db: Session = Depends(get_db)
):

    total = db.query(FocoDengue).count()

    resolvidos = db.query(FocoDengue)\
        .filter(FocoDengue.status == "Resolvido")\
        .count()

    pendentes = total - resolvidos

    tipos = db.query(
        FocoDengue.tipo,
        func.count(FocoDengue.id)
    ).group_by(
        FocoDengue.tipo
    ).all()

    por_tipo = {
        tipo: qtd
        for tipo, qtd in tipos
    }

    return {
        "total_focos": total,
        "resolvidos": resolvidos,
        "pendentes": pendentes,
        "por_tipo": por_tipo
    }


@router.get("/mapa")
def mapa(
    db: Session = Depends(get_db)
):

    focos = (
        db.query(FocoDengue)
        .filter(FocoDengue.status == "Pendente")
        .all()
    )

    return [
        {
            "id": foco.id,
            "tipo": foco.tipo,

            "latitude": foco.latitude,
            "longitude": foco.longitude,

            "rua": foco.rua,
            "numero": foco.numero,
            "bairro": foco.bairro,
            "complemento": foco.complemento,
            "cidade": foco.cidade,
            "estado": foco.estado,
            "cep": foco.cep,

            "status": foco.status,
            "data_criacao": foco.data_criacao
        }
        for foco in focos
    ]

@router.put("/focos/{id}/pendente")
def marcar_pendente(
    id: int,
    db: Session = Depends(get_db)
):

    foco = db.query(FocoDengue)\
        .filter(FocoDengue.id == id)\
        .first()

    if not foco:
        raise HTTPException(
            status_code=404,
            detail="Foco não encontrado"
        )

    foco.status = "Pendente"

    db.commit()

    return {
        "mensagem": "Foco marcado como pendente"
    }
