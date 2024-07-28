
class AppTheme(TypedDict):
    surface: str
    onSurface: str
    surfaceVariant: str
    onSurfaceVariant: str
    primary: str
    onPrimary: str

    danger: str
    onDanger: str


APP_THEME: AppTheme = {
    "surface": "#1a1625",
    "onSurface": "#ffffff",
    "surfaceVariant": "#76737e",
    "onSurfaceVariant": "#ffffff",
    "primary": "#382bf0",
    "onPrimary": "#ffffff",
    "danger": "#eb0c0c",
    "onDanger": "#ffffff"
}
