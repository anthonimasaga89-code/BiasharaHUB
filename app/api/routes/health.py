from fastapi import APIRouter

router = APIRouter(tags=["Health"])


def health_payload():
    return {"status": "ok", "service": "Biashara HUB API"}


@router.get("/health")
@router.get("/api/health")
def health():
    return health_payload()
