# BlackJack

こちらは、トランプゲーム **「BlackJack」** を遊べるWebアプリケーションです。

---

## BlackJackのルール

- プレイヤーとディーラーで手札を比べ、**手札の数字を足した合計がより21に近い方が勝利**となります。
- **合計が21を超えた場合**は、`Bust` となり負けが確定します。
- 絵札（J, Q, K）は、**10** として扱われます。
- A（エース）は、**1 または 11** として扱うことができます。

---

## ゲームの順序

1. **賭けチップを入力**してターンを開始します。
2. **プレイヤーとディーラー**にそれぞれ2枚ずつカードが配られます。
   - このとき、ディーラーのハンドは1枚だけ開示されます。
3. **プレイヤーのアクションフェーズ**:
   - プレイヤーは以下のアクションを選択できます:
     - **HIT**: カードを1枚追加で引く。
     - **STAND**: カードを引かずに勝負に進む。
   - プレイヤーは何枚でもカードを追加できますが、**Bust（合計が21を超える）**するとその時点で負けが確定します。
4. **ディーラーのアクションフェーズ**:
   - ディーラーは以下のルールに従って手札を確定します:
     - ハンドの合計が**17以上**になるまでカードを引き続けます。
5. **勝敗判定**:
   - 両者の手札を比べ、勝敗が決まります。

---

## 特徴

- Webブラウザ上でBlackJackを楽しめるインターフェース。
- シンプルで直感的な操作。
- ルールに基づいたディーラーの自動挙動。
