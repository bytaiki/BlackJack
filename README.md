# BlackJack

こちらは、トランプゲーム「 BlackJack 」を遊べるWebアプリケーションです。

BlackJackのルール:
・プレイヤーとディーラーで手札を比べ、手札の数字を足した数がより21に近い方の勝利となる
・足した合計が21を超えてしまった場合は、Bustとなり負けが確定する
・絵柄は、10 として扱われる
・A（エース）は、 1 と 11 どちらとしても扱える


　　　　　　　　　　　　　( ゲームの順序 )
賭けチップを入力してターンを開始する。
　　　　　　　　　　　　　　　　 ↓
プレイヤーとディーラーにそれぞれ2枚ずつ与えられ、ディーラーのハンドは１枚だけ開示される
　　　　　　　　　 　　　　　　　↓
まずプレイヤーがさらにカードを追加するかの選択肢が与えられ、
STAND(カードを追加せず勝負)を選択した時にディーラーのハンドを確定させるフェーズに移る。
何枚でもカードの追加はできるが、Bust(手札合計が21を超えた)した際は、負けが確定する。
　　　　　　　　　　　　　　　　 ↓
次は、ディーラーのハンドをルールに沿って確定させ、勝敗の結果を出す。

＊ディーラーのルールは、必ずハンドの合計が17以上になるまで
　カードを引かなければいけないというもの

