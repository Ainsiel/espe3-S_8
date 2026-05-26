# Reporte de Pruebas de Software (Test Report - EventPass)

- **Proyecto ID:** EJEMPLO_TRES
- **Suite:** Pytest (FastAPI TestClient)
- **Entorno de Aislamiento:** Sandbox Local

## Resultado
- **Estado General:** PASS

### Pytest Sandbox Execution Log
```text
============================= test session starts =============================
platform win32 -- Python 3.13.3, pytest-7.4.3, pluggy-1.6.0
rootdir: C:\Users\Ainsi\Desktop\proyectos\espe3-S_8
configfile: pytest.ini
plugins: anyio-4.11.0, Faker-20.1.0, cov-4.1.0, flask-1.3.0, mock-3.12.0
collected 18 items

tests\test_main.py ..................                                    [100%]

============================== warnings summary ===============================
..\..\..\..\..\..\AppData\Local\Programs\Python\Python313\Lib\site-packages\starlette\formparsers.py:12
  C:\Users\Ainsi\AppData\Local\Programs\Python\Python313\Lib\site-packages\starlette\formparsers.py:12: PendingDeprecationWarning: Please use `import python_multipart` instead.
    import multipart

app\main.py:17
  C:\Users\Ainsi\Desktop\proyectos\espe3-S_8\sandbox\EJEMPLO_TRES\backend\app\main.py:17: MovedIn20Warning: The ``declarative_base()`` function is now available as sqlalchemy.orm.declarative_base(). (deprecated since: 2.0) (Background on SQLAlchemy 2.0 at: https://sqlalche.me/e/b8d9)
    Base = declarative_base()

app\main.py:112
  C:\Users\Ainsi\Desktop\proyectos\espe3-S_8\sandbox\EJEMPLO_TRES\backend\app\main.py:112: PydanticDeprecatedSince20: Pydantic V1 style `@validator` validators are deprecated. You should migrate to Pydantic V2 style `@field_validator` validators, see the migration guide for more details. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.12/migration/
    @validator('email')

app\main.py:118
  C:\Users\Ainsi\Desktop\proyectos\espe3-S_8\sandbox\EJEMPLO_TRES\backend\app\main.py:118: PydanticDeprecatedSince20: Pydantic V1 style `@validator` validators are deprecated. You should migrate to Pydantic V2 style `@field_validator` validators, see the migration guide for more details. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.12/migration/
    @validator('password')

app\main.py:128
  C:\Users\Ainsi\Desktop\proyectos\espe3-S_8\sandbox\EJEMPLO_TRES\backend\app\main.py:128: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.12/migration/
    class UserResponse(BaseModel):

..\..\..\..\..\..\AppData\Local\Programs\Python\Python313\Lib\site-packages\pydantic\_internal\_config.py:383
  C:\Users\Ainsi\AppData\Local\Programs\Python\Python313\Lib\site-packages\pydantic\_internal\_config.py:383: UserWarning: Valid config keys have changed in V2:
  * 'orm_mode' has been renamed to 'from_attributes'
    warnings.warn(message, UserWarning)

app\main.py:136
  C:\Users\Ainsi\Desktop\proyectos\espe3-S_8\sandbox\EJEMPLO_TRES\backend\app\main.py:136: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.12/migration/
    class EventResponse(BaseModel):

app\main.py:156
  C:\Users\Ainsi\Desktop\proyectos\espe3-S_8\sandbox\EJEMPLO_TRES\backend\app\main.py:156: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.12/migration/
    class ReservationResponse(BaseModel):

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
======================= 18 passed, 8 warnings in 5.29s ========================


```