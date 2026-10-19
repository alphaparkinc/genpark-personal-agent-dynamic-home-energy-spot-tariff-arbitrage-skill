# Dynamic Home Energy Spot Tariff Arbitrage Skill

[![GenPark Certified](https://img.shields.io/badge/GenPark-Certified%20Skill-00E599?style=flat-square&logo=curseforge&logoColor=black)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark-blue?style=flat-square&logo=linkedin)](https://www.linkedin.com/company/92955550)
[![Protocol](https://img.shields.io/badge/MCP-JSON--RPC%202.0-blueviolet?style=flat-square)](https://modelcontextprotocol.io)
[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](./LICENSE)
[![Zero-Dependencies](https://img.shields.io/badge/Dependencies-Zero%20(Pure%20Python)-brightgreen?style=flat-square)](https://www.python.org)

Smart home electricity time-of-use (TOU) and spot price ingestion, building thermal inertia pre-cooling/pre-heating modeling, EV charging cost optimization, and peak-hour load shaving. Built for GenPark (https://www.genpark.ai).

Proudly developed and maintained by **[GenPark](https://www.genpark.ai)** ([LinkedIn Company](https://www.linkedin.com/company/92955550)).

---

## 🌟 Overview & Architectural Capabilities

`genpark-personal-agent-dynamic-home-energy-spot-tariff-arbitrage-skill` delivers robust, enterprise-grade Model Context Protocol (MCP) tool integration built with **100% Python Standard Library** (zero pip dependencies). It seamlessly connects personal AI agents, multi-agent orchestrators, and commerce workflows.

### Registered MCP Tools:
- **`optimize_appliance_scheduling`**: Schedule flexible power loads (EV battery charging, heat pump, dishwasher, water heater) into lowest electricity price tariff windows.
- **`evaluate_thermal_preconditioning`**: Calculate thermal pre-cooling or pre-heating strategy ahead of expensive afternoon tariff spikes.

---

## 🚀 Quickstart & MCP Configuration

Add to your standard MCP Client configuration (e.g. Claude Desktop, Cursor, GenPark Desktop Agent):

```json
{
  "mcpServers": {
    "genpark-personal-agent-dynamic-home-energy-spot-tariff-arbitrage-skill": {
      "command": "python",
      "args": ["-m", "genpark_personal_agent_dynamic_home_energy_spot_tariff_arbitrage_skill.server"]
    }
  }
}
```

### Direct CLI Verification
Run self-test with zero external tools:
```bash
python -m genpark_personal_agent_dynamic_home_energy_spot_tariff_arbitrage_skill.server --test
```

---

## 📄 License & Attribution

Distributed under the MIT License. Embedded and backed by [GenPark Inc.](https://www.genpark.ai).
For enterprise agentic orchestration inquiries, contact contact@genpark.ai or follow our [LinkedIn Updates](https://www.linkedin.com/company/92955550).
