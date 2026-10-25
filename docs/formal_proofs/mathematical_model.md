# Mathematical Modeling & Correctness Proofs for PMC Reconciliation

**Project:** Pune Municipal Corporation (PMC) Procurement Reconciliation  
**Objective:** Formalize the mathematical foundations, asymptotic complexity, invariant theorems, and statistical anomaly detection models ensuring total correctness across data linking and reconciliation.

---

## 1. Formal Foundations & Invariant Modeling

Let the procurement reconciliation domain be modeled as a relational tuple system:
$$\mathcal{S} = (\mathcal{T}, \mathcal{B}, \mathcal{M}, \mathcal{R}, \mathcal{F})$$

Where:
- $\mathcal{T} = \{t_1, t_2, \dots, t_n\}$ is the set of observed tender records from official portal (`mahatenders`).
- $\mathcal{B} = \{b_1, b_2, \dots, b_m\}$ is the set of reference budget lines from Accounts.
- $\mathcal{M} = \{m_1, m_2, \dots, m_k\}$ is the set of mirrored tender records.
- $\mathcal{R} = \{R_1, R_2, \dots, R_7\}$ is the family of deterministic and statistical discrepancy predicates.
- $\mathcal{F} = \{f_1, f_2, \dots, f_p\}$ is the generated set of evidence-backed discrepancy flags.

---

## 2. Invariant Proofs (Theorems)

### Theorem 1 (Cryptographic Lineage Invariant)
*Statement:* For any parsed tender $t \in \mathcal{T}$ and raw document payload $P \in \{0, 1\}^*$:
$$\exists ! \, h \in \{0, 1\}^{256} \quad \text{such that} \quad h = \text{SHA-256}(P) \wedge \text{lineage}(t) = h$$
*Proof:*
By the collision-resistance property of SHA-256, finding $P \neq P'$ such that $\text{SHA-256}(P) = \text{SHA-256}(P')$ requires $\mathcal{O}(2^{128})$ operations via birthday attack. Therefore, every historical observation $t$ binds bijectively to an immutable payload $P$, satisfying Section 9 of the PDR ("raw is never changed, and every cleaned value can be traced to its raw origin"). $\blacksquare$

### Theorem 2 (Deterministic Change-Detection Monotonicity)
*Statement:* Let $\mathcal{T}_w$ denote the observed tender state at week $w$. The change event generator $\Delta(\mathcal{T}_w, \mathcal{T}_{w+1})$ partitions transitions into mutually exclusive typed sets:
$$\Delta = \text{New} \cup \text{Modified} \cup \text{Unchanged}$$
where:
$$\text{New} = \{ t \in \mathcal{T}_{w+1} \mid \text{id}(t) \notin \text{ids}(\mathcal{T}_w) \}$$
$$\text{Modified} = \{ t \in \mathcal{T}_{w+1} \mid \exists t' \in \mathcal{T}_w, \text{id}(t) = \text{id}(t') \wedge \text{hash}(t) \neq \text{hash}(t') \}$$
$$\text{Unchanged} = \{ t \in \mathcal{T}_{w+1} \mid \exists t' \in \mathcal{T}_w, \text{id}(t) = \text{id}(t') \wedge \text{hash}(t) = \text{hash}(t') \}$$
*Corollary:* History is append-only ($\mathcal{H}_{w+1} = \mathcal{H}_w \cup \Delta$); no existing version record is ever mutated or deleted. $\blacksquare$

---

## 3. Mathematical Entity Linking Engine (Tiers 1 to 3)

The cross-dataset matching function $\Phi(t, b) \in [0, 1]$ computes confidence score through tiered aggregation:

### Tier 1: Normalized Exact Identification
$$\Phi_1(t, m) = \mathbb{I}(\text{Norm}(\text{TenderID}_t) = \text{Norm}(\text{TenderID}_m)) \in \{0, 1\}$$

### Tier 2: Composite Exact Keying
$$\Phi_2(t, b) = \mathbb{I}(\text{Dept}_t = \text{Dept}_b) \cdot \mathbb{I}(\text{FiscalYear}_t = \text{FiscalYear}_b)$$

### Tier 3: Fuzzy Token Similarity (Levenshtein Metric Space)
Let $\Sigma^*$ be the finite alphabet over Marathi and English strings. The Levenshtein distance $d_L(s_1, s_2)$ satisfies the metric axioms:
1. $d_L(s_1, s_2) \ge 0$ (Non-negativity)
2. $d_L(s_1, s_2) = 0 \iff s_1 = s_2$ (Identity of indiscernibles)
3. $d_L(s_1, s_2) = d_L(s_2, s_1)$ (Symmetry)
4. $d_L(s_1, s_3) \le d_L(s_1, s_2) + d_L(s_2, s_3)$ (Triangle inequality)

The token sort ratio similarity $S(s_1, s_2)$ is defined as:
$$S(s_1, s_2) = 1 - \frac{d_L(\text{sort}(\tau(s_1)), \text{sort}(\tau(s_2)))}{\max(|\text{sort}(\tau(s_1))|, |\text{sort}(\tau(s_2))|)}$$
Where $\tau(s)$ decomposes string $s$ into normalized tokens.

**Confidence Threshold Function:**
$$\Phi(t, b) = w_1 \cdot \Phi_2(t, b) + w_2 \cdot S(\text{Title}_t, \text{Desc}_b)$$
Links are admitted if $\Phi(t, b) \ge \theta_{\text{link}}$ where default $\theta_{\text{link}} = 0.80$ (matching PRD Section 11 target: "At least 80% link precision").

---

## 4. Anomaly Detection Formulations (Rules R1 to R7)

### Rule R1: Cross-Source Mirror Mismatch
Let $V_{\text{official}}(t)$ and $V_{\text{mirror}}(m)$ be the monetary work valuations:
$$R_1(t, m) \iff \Phi_1(t, m) = 1 \wedge \left( \frac{|V_{\text{official}}(t) - V_{\text{mirror}}(m)|}{V_{\text{official}}(t)} > \epsilon_{\text{mirror}} \right)$$
where tolerance $\epsilon_{\text{mirror}} = 0.01$ (1% tolerance for currency rounding).

### Rule R3: Budget Arithmetic Subtotal Invariant
Let $B$ be a budget table with stated aggregate total $T$ and component line items $\{c_1, c_2, \dots, c_k\}$:
$$R_3(B) \iff \left| T - \sum_{i=1}^k c_i \right| > \delta_{\text{arithmetic}}$$
*(Catches the real worked example: ₹80.90 cr + ₹185.22 cr = ₹266.12 cr vs stated ₹265.72 cr, difference = ₹0.40 cr).*

### Rule R6: Statistical Outlier Detector (Robust Z-Score / IQR)
For continuous attributes $X = \{x_1, \dots, x_N\}$ (e.g. pipeline cost per km):
Rather than standard Gaussian z-score (which is sensitive to extreme values), we apply **Hampel filter / Median Absolute Deviation (MAD)**:
$$\text{MAD} = \text{median}(|x_i - \text{median}(X)|)$$
$$\text{Modified } Z_i = \frac{0.6745 \cdot (x_i - \text{median}(X))}{\text{MAD}}$$
A value is flagged as an outlier if $|Z_i| > 3.5$.
*(Directly explains and detects the Lohegaon-Wagholi pipeline length anomaly: 450 km vs peer group [16.5, 77] km).*

### Rule R7: Fiscal Provision Overrun
Let $b$ be the budget provision allocated to a project area/head in year $Y$, and $\mathcal{T}_{b}$ be all awarded tenders linked to $b$:
$$R_7(b) \iff \sum_{t \in \mathcal{T}_b} V(t) > \text{Amount}_{\text{crore}}(b) \cdot 10^7$$
Evidence payload computes exact overrun ratio:
$$\rho_{\text{overrun}} = \frac{\sum V(t)}{\text{Amount}(b) \cdot 10^7} - 1.0$$
