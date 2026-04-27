Progress on scenario 03 ✅ but still failing on 01 and 02. Let me score this run :

---

### Scenario 01 ❌
Called individual tools instead of `run_pipeline` — still going step by step.

### Scenario 02 ❌
Still dumps all fields at once including `finding_active` and `finding_verified` — forbidden fields still appear.

### Scenario 03 ⚠️ Partial progress
Memory works across turns ✅, correctly collects `finding_found_by` ✅, but still asks **"Do you want to continue?"** and lists multiple fields at once ❌.

---

### Updated score comparison

| Criteria | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| Extracts fields | ⚠️ 50% | ⚠️ 50% | ⚠️ 60% |
| One field at a time | ❌ 0% | ❌ 0% | ❌ 0% |
| Uses run_pipeline | ❌ 0% | ❌ 0% | ❌ 0% |
| Remembers context | ⚠️ 50% | ⚠️ 50% | ✅ 70% |
| Never invents fields | ❌ 0% | ❌ 0% | ⚠️ 50% |
| **Total** | **~20/100** | **~20/100** | **~36/100** |

---

### Conclusion

The prompt improvements are helping incrementally but **qwen2.5:7b has hit its ceiling**. The two problems that never improve — `run_pipeline` usage and one-field-at-a-time — require a stronger model to follow reliably.

**Run the 14b benchmark now** — this is exactly the data you need to justify the upgrade.