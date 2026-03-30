# 🚀 3GPP Search Agent: Protocol Analysis Example

This document demonstrates the capabilities of the **3GPP Search Agent** in automating the extraction and transformation of complex telecommunications specifications into developer-ready insights.

## 🔍 The Scenario
**User Query:** *PDU SESSION RESOURCE SETUP REQUEST*

---
Query Result: Based on the provided `<spec_file_context>`, here is the protocol analysis for the **PDU SESSION RESOURCE SETUP REQUEST** message.

### Functional Role
This message is sent by the AMF (Access and Mobility Management Function) to the target NG-RAN node to request the preparation of resources.
**Direction:** AMF $\rightarrow$ NG-RAN node.

### ASN.1 Definition (Extracted Fragments)
The provided context includes fragmented ASN.1 definitions primarily covering the internal `PDU Session Resource Setup Item` elements belonging to the request.

```asn1
-- PDU Session Resource Setup Item (Reconstructed from Context)
SEQUENCE {
    pDUSessionID                               PDUSessionID,
    nAS-PDU                                    NAS-PDU OPTIONAL,
    s-NSSAI                                    S-NSSAI,
    pDUSessionResourceSetupRequestTransfer     OCTET STRING (CONTAINING PDUSessionResourceSetupRequestTransfer),
    iE-Extensions                              ProtocolExtensionContainer { {PDUSessionResourceSetupItemCxtReq-ExtIEs} } OPTIONAL,
    ...
}

PDUSessionResourceSetupItemCxtReq-ExtIEs NGAP-PROTOCOL-EXTENSION ::= {
    { ID id-PduSessionExpectedUEActivityBehaviour CRITICALITY ignore EXTENSION ExpectedUEActivityBehaviour PRESENCE optional },
    ...
}
```
*Note: The context also contains snippets for `PDUSessionResourceSetupItemCxtRes` which is part of the Response message, not the Request.*

### Technical Attributes Table

Based on the explicit tabular data provided in the context, the contents defining the setup request (or related handover context) include the following Information Elements (IEs):

| IE/Group Name | Presence | Data Type / Reference | Semantics Description / Range |
| :--- | :---: | :--- | :--- |
| Message Type | M | - | - |
| AMF UE NGAP ID | M | - | - |
| Handover Type | M | - | - |
| Cause | M | - | - |
| UE Aggregate Maximum Bit Rate | M | - | - |
| Core Network Assistance Information for RRC INACTIVE | O | - | - |
| UE Security Capabilities | M | - | - |
| Security Context | M | - | - |
| New Security Context Indicator | O | - | - |
| NASC | O | - | - |
| PDU Session Resource Setup List | O | SEQUENCE OF | Size constraint: $1 \leq \text{size} \leq \text{maxnoofPDUSessions}$ |
| > PDU Session Resource Setup Item | - | SEQUENCE | - |
| >> PDU Session ID | - | PDUSessionID | - |
| >> S-NSSAI | - | S-NSSAI | - |
| >> Handover Request Transfer | - | OCTET STRING | Defined in ASN.1 as `pDUSessionResourceSetupRequestTransfer` |
| >> PDU Session Expected UE Activity Behaviour | O | ExpectedUEActivityBehaviour | Provided via `ProtocolExtensionContainer` |
| Allowed NSSAI | O | - | - |

*(Note: "M" = Mandatory, "O" = Optional. Blank presence codes for nested list elements imply they are governed by the presence of the parent List/Sequence.)*

### Suggested JSON Implementation

Below is a conceptual JSON payload representing the `PDU SESSION RESOURCE SETUP REQUEST` message, utilizing the exact structure mapped out in the tabular and ASN.1 context.   

```json
{
  "PDUSessionResourceSetupRequest": {
    "messageType": "PDU_SESSION_RESOURCE_SETUP_REQUEST",
    "amfUeNgapId": 123456789,
    "handoverType": "Intra5G",
    "cause": {
      "radioNetwork": "handover-desirable-for-radio-reasons"
    },
    "ueAggregateMaximumBitRate": {
      "uEaggregateMaximumBitRateDL": 100000000,
      "uEaggregateMaximumBitRateUL": 50000000
    },
    "ueSecurityCapabilities": {
      "nRencryptionAlgorithms": "C000",
      "nRintegrityProtectionAlgorithms": "C000",
      "eUTRAencryptionAlgorithms": "C000",
      "eUTRAintegrityProtectionAlgorithms": "C000"
    },
    "securityContext": {
      "nextHopChainingCount": 2,
      "nextHopNH": "a1b2c3d4e5f6..."
    },
    "newSecurityContextIndicator": true,
    "pduSessionResourceSetupList": [
      {
        "pduSessionId": 1,
        "nAS-PDU": "0102030405...",
        "s-NSSAI": {
          "sST": 1,
          "sD": "000001"
        },
        "handoverRequestTransfer": "abcdef123456...",
        "pduSessionExpectedUEActivityBehaviour": {
          "expectedActivityPeriod": 30,
          "expectedIdlePeriod": 120
        }
      }
    ],
    "allowedNSSAI": [
      {
        "sST": 1,
        "sD": "000001"
      }
    ]
  }
}
```