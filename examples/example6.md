# 🚀 3GPP Search Agent: Protocol Analysis Example

This document demonstrates the capabilities of the **3GPP Search Agent** in automating the extraction and transformation of complex telecommunications specifications into developer-ready insights.

## 🔍 The Scenario
**User Query:** *Last Visited E-UTRAN Cell Information*

---
Query Result: Based on the provided specification context (TS 36.413 / S1AP), here is the analysis for the **Last Visited E-UTRAN Cell Information** Information Element (IE). 

### Functional Role
The `Last Visited E-UTRAN Cell Information` IE contains information about a specific E-UTRAN cell that the UE has previously visited. This information is utilized primarily for Radio Resource Management (RRM) purposes, including tracking the time the UE stayed in the cell and identifying handover causes.

### ASN.1 Definition
Based on the provided context, the ASN.1 syntax for this IE and its extensions is defined as follows:

```asn1
global-Cell-ID             EUTRAN-CGI,
cellType                   CellType,
time-UE-StayedInCell       Time-UE-StayedInCell,
iE-Extensions              ProtocolExtensionContainer { { LastVisitedEUTRANCellInformation-ExtIEs} } OPTIONAL,
}

LastVisitedEUTRANCellInformation-ExtIEs S1AP-PROTOCOL-EXTENSION ::= {
-- Extension for Rel-11 to support enhanced granularity for time UE stayed in cell --
{ ID id-Time-UE-StayedInCell-EnhancedGranularity CRITICALITY ignore  EXTENSION Time-UE-StayedInCell-EnhancedGranularity  PRESENCE optional}|
{ ID id-HO-Cause                                 CRITICALITY ignore  EXTENSION Cause                                     PRESENCE optional}|
{ ID id-lastVisitedPSCellList                    CRITICALITY ignore  EXTENSION LastVisitedPSCellList                     PRESENCE optional},
...
}

LastVisitedPSCellList  ::= SEQUENCE (SIZE(1.. maxnoofPSCellsPerPrimaryCellinUEHistoryInfo)) OF LastVisitedPSCellInformation
```

### Technical Attributes

| IE/Group Name | Presence | Data Type & Reference | Value Range | Semantics Description |
| :--- | :---: | :--- | :--- | :--- |
| **Global Cell ID** | M | E-UTRAN CGI | N/A | Globally unique identifier for the E-UTRAN cell. |
| **Cell Type** | M | CellType | N/A | The type of the cell visited. |
| **Time UE stayed in Cell** | M | INTEGER | $0 \dots 4095$ | Duration the UE stayed in the cell in seconds. If time $t > 4095$ seconds, this IE is capped at $4095$. |        
| **Time UE stayed in Cell Enhanced Granularity** *(via Extension)* | O | INTEGER | $0 \dots 40950$ | Duration the UE stayed in the cell in $1/10$ seconds. If time $t > 4095$ seconds, this IE is capped at $40950$. |
| **HO Cause Value** *(via Extension)* | O | Cause | N/A | The cause for the handover from the E-UTRAN cell. |
| **Last Visited PSCell List** *(via Extension)* | $0 \dots 8$ | SEQUENCE OF LastVisitedPSCellInformation | $1 \dots \text{max}$ | List of cells configured as PSCells. Most recent PSCell info is at the top. Maximum size is `maxnoofPSCellsPerPrimaryCellinUEHistoryInfo` ($8$). |

### Suggested JSON Implementation
Below is a suggested JSON payload structure representing a UE that stayed in a cell for $120.5$ seconds, capturing both standard and enhanced granularity timers, along with PSCell history.

```json
{
  "LastVisitedEUTRANCellInformation": {
    "global-Cell-ID": {
      "plmn-Identity": "20810",
      "cellIdentity": "0A1B2C3"
    },
    "cellType": {
      "cell-Size": "macro"
    },
    "time-UE-StayedInCell": 120,
    "iE-Extensions": {
      "Time-UE-StayedInCell-EnhancedGranularity": 1205,
      "Cause": {
        "radioNetwork": "handover-desirable-for-radio-reasons"
      },
      "LastVisitedPSCellList": [
        {
          "LastVisitedPSCellInformation": {
            "global-Cell-ID": {
              "plmn-Identity": "20810",
              "cellIdentity": "0D4E5F6"
            }
          }
        }
      ]
    }
  }
}
```