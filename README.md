# 🧩 Domain Mapper for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/hacs/integration)
[![GitHub release](https://img.shields.io/github/v/release/lunDreame/domain-mapper)](https://github.com/lunDreame/domain-mapper/releases)
[![GitHub stars](https://img.shields.io/github/stars/lunDreame/domain-mapper)](https://github.com/lunDreame/domain-mapper/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/lunDreame/domain-mapper)](https://github.com/lunDreame/domain-mapper/issues)

> Map entities from one domain to another in Home Assistant (e.g., `water_heater` → `climate`, `sensor` → `binary_sensor`)

---

## ✨ Features

- 🔁 Map one entity to another domain
- 🌡️ Attribute-based proxy creation (e.g. temperature, state)
- 🔧 Works with `climate`, `binary_sensor`, and more to come
- 🔄 Sync state automatically with the source entity
- ⚙️ Supports `config_flow` and `options_flow`

---

## 📦 Installation

### ✔️ Install via HACS (Recommended)

1. Make sure [HACS](https://hacs.xyz) is installed.
2. Go to **HACS > Integrations**.
3. Click the three-dot menu (⋮) → **"Custom repositories"**.
4. Add the following URL as an Integration: https://github.com/lunDreame/domain-mapper
5. Search for `Domain Mapper` and install.
6. Restart Home Assistant.

### 📁 Manual Installation

1. Download the repository as ZIP or clone it:
```bash
git clone https://github.com/lunDreame/domain-mapper
```
2. Copy the folder to your custom components directory:
```
/config/custom_components/domain_mapper/
```
3. Restart Home Assistant.

---

## ⚙️ Configuration

1. Go to **Settings > Devices & Services > Add Integration.**
2. Search for Domain Mapper.
3. Follow the guided setup:
    - **Source Domain**: The domain of the original entity (e.g., water_heater)
    - **Target Domain**: The domain to expose (e.g., climate)
    - **Source Entity**: The original entity ID
    - **Property Name**: Attribute to extract (e.g., temperature, state)
    - **Property Device Class**: Optional for sensor-based mapping

---

## 🔍 Example Use Case

**Map water_heater.boiler → climate.boiler_mapper**
```yaml
- source_entity: water_heater.boiler
- target_domain: climate
- property_name: temperature
- property_device_class: temperature
```
This allows using the entity in thermostat UIs or automations requiring a climate device.

---

## 📄 Links

- [🔗 GitHub Repository](https://github.com/lunDreame/domain-mapper)
- [🛠️ Report Issues](https://github.com/lunDreame/domain-mapper/issues)
- [🧩 HACS Docs](https://hacs.xyz/docs)

---

## 🙋 Support
If you find this useful, consider giving a ⭐ on GitHub and submitting issues or feature requests.
