# 🚀 3GPP Search Agent: Protocol Analysis Example

This document demonstrates the capabilities of the **3GPP Search Agent** in automating the extraction and transformation of complex telecommunications specifications into developer-ready insights.

## 🔍 The Scenario
**User Query:** *Handover Restriction List* IE.

### Functional Role
The `Handover Restriction List` provides the eNB with UE-specific mobility and access restrictions. This information, received from the core network in a `DOWNLINK NAS TRANSPORT` message, is stored in the UE context. The eNB uses this list to make decisions for subsequent mobility actions, such as determining a suitable handover target or selecting a Secondary Cell Group (SCG) during dual connectivity operations. It ensures that the UE is only handed over to cells and PLMNs where it is allowed to operate.

### Data Type
The IE is a structured list, defined in ASN.1 as a `SEQUENCE`.

### Presence/Need Code
The IE is **Optional** (Need N) in messages like `HANDOVER REQUEST` and `DOWNLINK NAS TRANSPORT`. The procedural text states, "If the target eNB receives a HANDOVER REQUEST message which does not contain the Handover Restriction List IE..." and "...if present in the DOWNLINK NAS TRANSPORT message," which confirms its optional nature.

### Value Range
Not applicable for the `SEQUENCE` itself. The value range applies to its constituent fields, such as the `Equivalent PLMNs` list.

---

### ASN.1 Field Description

| IE/Group Name | Presence | Range | IE Type and Reference | Semantics Description |
| :--- | :--- | :--- | :--- | :--- |
| **Handover Restriction List** | | | **SEQUENCE** | |
| > Serving PLMN | M | | PLMNidentity (9.2.3.8) | The primary PLMN where the UE is currently served. |
| > Equivalent PLMNs | O | 0..<`maxnoofEPLMNs`> | SEQUENCE (OF PLMNidentity) | A list of PLMNs considered equivalent to the Serving PLMN for cell selection/reselection. |      
| > NRrestrictioninEPSasSecondaryRAT | O | | NRrestrictioninEPSasSecondaryRAT | Specifies restrictions for using NR as a secondary RAT in an EPS/E-UTRA context. |
| > UnlicensedSpectrumRestriction | O | | UnlicensedSpectrumRestriction | Specifies restrictions related to the use of unlicensed spectrum. |
| > CNTypeRestrictions | O | | CNTypeRestrictions | Specifies restrictions based on the Core Network type (e.g., EPC, 5GC). |
| > NRrestrictionin5GS | O | | NRrestrictionin5GS | Specifies restrictions for using NR within the 5G System. |
| > LastNG-RANPLMNIdentity | O | | PLMNidentity | The PLMN Identity of the last visited NG-RAN cell. |
| > RAT-Restrictions | O | | RAT-Restrictions | A list of forbidden RAT types for the UE. |

---

### Suggested JSON Implementation

This JSON object represents a potential implementation of the `Handover Restriction List`, with some optional fields populated for illustrative purposes.

```json
{
  "handoverRestrictionList": {
    "servingPLMN": "262-01",
    "equivalentPLMNs": [
      "262-02",
      "234-15"
    ],
    // -- Optional Fields Below --
    "nrRestrictionInEPSasSecondaryRAT": "nr-as-secondary-rat-restricted",
    "unlicensedSpectrumRestriction": null,
    "cnTypeRestrictions": [
      "epc-forbidden"
    ],
    "nrRestrictionIn5GS": null,
    "lastNgRanPlmnIdentity": "208-93",
    "rat-Restrictions": [
      "eutra",
      "utran"
    ]
  }
}
```