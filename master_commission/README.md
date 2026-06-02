# Master Commission: Profit Sharing & Liquidations

Calculate and distribute sales commissions to your business partners based on actual profit margins, not just gross revenue.

## Features
- **Margin-Based Commissions**: Automates profit calculations upon Sales Order confirmation.
- **Partner Management**: Define specific split percentages for each partner involved in a sale.
- **Monthly Liquidations**: Automatically generate accounting Vendor Bills to pay your partners at the end of the month.
- **Transparency**: Partners can access their own portal to track pending and paid commissions.
- **Dashboard**: Get a clear overview of the generated utility and commissions owed.

## Configuration
1. Go to **Sales > Master Commission > Settings** to configure default journals and accounts for liquidations.
2. In **Sales > Master Commission > Partners**, register the internal or external users who will receive commissions.
3. Configure the products' cost and sale prices properly, as commissions are calculated based on utility (`Sale Price - Cost`).

## Usage
1. Create a Sales Order.
2. Add products.
3. In the "Partners" tab, add the users who will split the profit of this specific order.
4. Confirm the Sales Order. The system will automatically generate the commission records for each partner.
5. At the end of the month, go to **Liquidations** and create a new record to consolidate the unpaid commissions into a draft Vendor Bill.

---
**Developed by:** JDDM
