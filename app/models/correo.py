from odmantic import Field, Model
from pydantic import EmailStr


class Correo(Model):
    direccion: EmailStr
