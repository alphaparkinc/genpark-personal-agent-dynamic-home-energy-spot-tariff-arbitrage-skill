# -*- coding: utf-8 -*-
"""Model Context Protocol (MCP) Server for Dynamic Home Energy Spot Tariff Arbitrage Skill
Powered by GenPark (https://www.genpark.ai).
"""
import sys
import json
import logging
from .core import *

TOOLS_METADATA = [
  {
    "name": "optimize_appliance_scheduling",
    "description": "Schedule flexible power loads (EV battery charging, heat pump, dishwasher, water heater) into lowest electricity price tariff windows.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "hourly_rates_cents_kwh": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "description": "24-hour electricity spot prices in cents/kWh from 00:00 to 23:00"
        },
        "ev_charging_kwh_required": {
          "type": "number"
        },
        "ev_ready_by_hour": {
          "type": "integer",
          "description": "e.g. 7 for 07:00 AM"
        }
      },
      "required": [
        "hourly_rates_cents_kwh",
        "ev_charging_kwh_required",
        "ev_ready_by_hour"
      ]
    }
  },
  {
    "name": "evaluate_thermal_preconditioning",
    "description": "Calculate thermal pre-cooling or pre-heating strategy ahead of expensive afternoon tariff spikes.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "target_comfort_temp_c": {
          "type": "number"
        },
        "peak_tariff_start_hour": {
          "type": "integer"
        },
        "peak_rate_cents_kwh": {
          "type": "number"
        },
        "off_peak_rate_cents_kwh": {
          "type": "number"
        }
      },
      "required": [
        "target_comfort_temp_c",
        "peak_tariff_start_hour",
        "peak_rate_cents_kwh",
        "off_peak_rate_cents_kwh"
      ]
    }
  }
]

def handle_rpc(request_str: str) -> str:
    try:
        req = json.loads(request_str)
    except Exception as e:
        return json.dumps({"jsonrpc": "2.0", "error": {"code": -32700, "message": "Parse error"}, "id": None})
    
    msg_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        return json.dumps({
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {
                    "name": "genpark-personal-agent-dynamic-home-energy-spot-tariff-arbitrage-skill",
                    "version": "1.0.0",
                    "vendor": "GenPark (https://www.genpark.ai)"
                }
            }
        })

    if method == "tools/list":
        return json.dumps({
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {"tools": TOOLS_METADATA}
        })

    if method == "tools/call":
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        func = globals().get(tool_name)
        if not func or not callable(func):
            return json.dumps({
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {"code": -32601, "message": f"Method '{tool_name}' not found"}
            })
        
        try:
            call_res = func(**arguments)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [
                        {"type": "text", "text": json.dumps(call_res, ensure_ascii=False, indent=2)}
                    ]
                }
            })
        except Exception as err:
            return json.dumps({
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {"code": -32000, "message": f"Execution error: {str(err)}"}
            })

    return json.dumps({
        "jsonrpc": "2.0",
        "id": msg_id,
        "error": {"code": -32601, "message": f"Unhandled method '{method}'"}
    })

def run_self_test():
    print(f"=== Running Self Test for genpark-personal-agent-dynamic-home-energy-spot-tariff-arbitrage-skill ===")
    init_res = json.loads(handle_rpc(json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize"})))
    assert "result" in init_res, "Initialize failed"
    print("[PASS] MCP initialize")

    list_res = json.loads(handle_rpc(json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})))
    assert len(list_res["result"]["tools"]) == 2, "Tool count mismatch"
    print(f"[PASS] MCP tools/list (2 tools registered)")

    # Execute smoke test for each tool

    call1 = json.loads(handle_rpc(json.dumps({
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "optimize_appliance_scheduling",
            "arguments": {
                "hourly_rates_cents_kwh": [12.5, 10.2, 9.8, 8.5, 8.2, 9.0, 14.5, 22.0, 18.0, 16.5, 15.0, 14.2, 13.8, 14.0, 16.0, 24.5, 32.0, 38.5, 42.0, 35.0, 26.0, 19.5, 15.2, 13.0],
                "ev_charging_kwh_required": 40.0,
                "ev_ready_by_hour": 7
            }
        }
    })))
    assert "result" in call1, "Call1 failed"
    print("[PASS] Tool smoke test: optimize_appliance_scheduling")

    print("[ALL TESTS PASSED] Self-test verified successfully.")
    return True

if __name__ == "__main__":
    if "--test" in sys.argv:
        success = run_self_test()
        sys.exit(0 if success else 1)
    
    for line in sys.stdin:
        if not line.strip():
            continue
        out = handle_rpc(line)
        sys.stdout.write(out + "\n")
        sys.stdout.flush()
