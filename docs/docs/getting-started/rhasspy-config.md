# Rhasspy Config
```python
class RhasspySettings(BaseModel):
    url: AnyHttpUrl = "http://rhasspy:12101"
    mqtt_host: str = "rhasspy"
    mqtt_port: int = 12183
    mqtt_username: Optional[str] = None
    mqtt_password: Optional[str] = None
    microphone_device: Optional[str] = None
    sounds_device: Optional[str] = None
```

Still needs to be properly documented...