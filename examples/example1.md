# 🚀 3GPP Search Agent: Protocol Analysis Example

This document demonstrates the capabilities of the **3GPP Search Agent** in automating the extraction and transformation of complex telecommunications specifications into developer-ready insights.

## 🔍 The Scenario
**User Query:** *Registration reject*

---

Query Result: Based on the provided context from 3GPP TS 24.501, here is the analysis of the **REGISTRATION REJECT** message.

The `REGISTRATION REJECT` is a 5G Mobility Management (5GMM) message sent by the network (AMF) to the UE to reject a registration procedure. The message structure and its constituent Information Elements (IEs) are defined in the provided context.

It's important to note that 3GPP NAS protocols, such as the one defined in TS 24.501, use a Type/Length/Value (TLV) or Value (V) format for encoding messages, not ASN.1 syntax, which is typically used in RRC protocols (TS 38.331/36.331).

### **REGISTRATION REJECT Message**

#### **1. Functional Role**
The primary function of the `REGISTRATION REJECT` message is to inform the UE that its request for registration to the 5G network has been denied. It mandatorily includes a `5GMM cause` value to specify the reason for the rejection. The message can also carry optional information, such as back-off timers (`T3346`, `T3502`) or information about network slicing (`Rejected NSSAI`), to guide the UE's subsequent actions.

#### **2. Field Descriptions**
The following table details the Information Elements (IEs) that can be included in the `REGISTRATION REJECT` message, as specified in `Table 8.2.9.1.1`.

| Information Element (IE) | Presence | Format | Length (Octets) | Functional Role |
| :--- | :--- | :--- | :--- | :--- |
| **Extended protocol discriminator** | M | V | 1 | Identifies the message as part of the 5GMM protocol. |
| **Security header type** | M | V | 1/2 | Specifies the type of security protection applied to the message (e.g., plain, integrity protected). |
| **Spare half octet** | M | V | 1/2 | A reserved field, not currently used. |
| **Registration reject message identity** | M | V | 1 | Identifies the message type as `REGISTRATION REJECT`. |
| **5GMM cause** | M | V | 1 | Provides the specific reason for the registration failure. |
| **T3346 value** | O | TLV | 3 | Specifies a back-off timer value that the UE must wait before re-initiating registration in the current PLMN. |
| **T3502 value** | O | TLV | 3 | Specifies a back-off timer value for initiating registration for mobility or periodic update in the current PLMN. |
| **EAP message** | O | TLV-E | 7-1503 | Carries an Extensible Authentication Protocol (EAP) message for authentication/re-authentication purposes. |
| **Rejected NSSAI** | O | TLV | 4-42 | Contains a list of S-NSSAIs that were rejected by the network from the UE's requested NSSAI. |
| **CAG information list** | O | TLV-E | 3-n | Provides information about Closed Access Groups (CAGs). |
| **Extended rejected NSSAI** | O | TLV | 5-90 | Provides an extended list of rejected S-NSSAIs. |
| **Disaster return wait range** | O | TLV | 4 | Informs the UE of a wait time range before it can re-attempt access during a disaster roaming scenario. |

**Key:**
- **M**: Mandatory
- **O**: Optional
- **V**: Value only format
- **TLV**: Type-Length-Value format
- **TLV-E**: Type-Length-Value format with an extended length field

---

#### **3. Suggested JSON Implementation**
Below is a sample JSON object representing a `REGISTRATION REJECT` message. This example illustrates how the defined structure could be implemented in a modern, human-readable format, including both mandatory and optional fields.

```json
{
  "messageName": "REGISTRATION_REJECT",
  "extendedProtocolDiscriminator": "5GMM_MESSAGE",
  "securityHeaderType": "PLAIN_5GS_NAS_MESSAGE",
  "messageIdentity": "REGISTRATION_REJECT",
  "5gmmCause": "ILLEGAL_UE",
  "optionalFields": {
    "t3346Value": {
      "unit": "DEACTIVATED",
      "timerValue": 0
    },
    "rejectedNssai": [
      {
        "sst": 1,
        "sd": "000001"
      }
    ]
  }
}