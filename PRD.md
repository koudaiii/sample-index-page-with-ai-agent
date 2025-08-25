# Planning Guide

コンテンツプラットフォームのメインインデックス画面で、ユーザーが商品やおすすめ企画、新着コンテンツを効率的に発見し閲覧できるハブとして機能する。

**Experience Qualities**: 
1. **Discoverable** - ユーザーが様々なコンテンツを自然に発見できる直感的な構造
2. **Engaging** - 動的なバナーとビジュアル重視のレイアウトでユーザーの関心を引く
3. **Organized** - 情報が整理され、目的のコンテンツにスムーズにアクセスできる

**Complexity Level**: 
- Light Application (multiple features with basic state)
  - 複数のコンテンツセクション、自動ローテーションバナー、ナビゲーション機能を含むが、ユーザーアカウントや複雑な状態管理は不要

## Essential Features

### グローバルヘッダー
- **Functionality**: サイトナビゲーション、ロゴ、検索機能を提供
- **Purpose**: ユーザーがサイト全体をナビゲートできる一貫したインターフェース
- **Trigger**: ページロード時に表示
- **Progression**: ページ表示 → ヘッダー固定表示 → ナビゲーションアクセス可能
- **Success criteria**: ヘッダーが全画面で表示され、ナビゲーション要素がクリック可能

### ローテーションバナー
- **Functionality**: おすすめコンテンツや広告を3秒間隔で自動ローテーション表示
- **Purpose**: 重要なコンテンツや新着情報をユーザーに効果的にアピール
- **Trigger**: ページロード後、自動でローテーション開始
- **Progression**: 初期バナー表示 → 3秒後フェード切り替え → 次バナー表示 → ループ継続
- **Success criteria**: 3つのバナーが滑らかに切り替わり、ユーザーが手動でも操作可能

### コンテンツリスト
- **Functionality**: 商品、おすすめ品、新企画などを整理されたグリッドで表示
- **Purpose**: ユーザーが興味のあるコンテンツを効率的にブラウズできる
- **Trigger**: ページロード時に表示
- **Progression**: ページロード → コンテンツ取得 → グリッド表示 → アイテムクリック可能
- **Success criteria**: コンテンツが適切にカテゴリ分けされ、レスポンシブなグリッドで表示

## Edge Case Handling

- **画像読み込み失敗**: プレースホルダー画像で代替表示
- **コンテンツ空状態**: 「準備中」メッセージと代替コンテンツを表示
- **ネットワーク遅延**: ローディング状態とスケルトン UI を表示
- **小画面対応**: モバイルでバナーとグリッドが適切にスタック表示

## Design Direction

モダンで洗練されたEコマース風のデザインで、商品発見の楽しさを演出し、ユーザーが長時間滞在したくなる魅力的な空間を創出する。ミニマルながらもビジュアルが豊富なインターフェースで機能性と美しさを両立。

## Color Selection

Analogous (adjacent colors on color wheel) - 暖色系の類似色を使用してコンテンツの魅力を引き立て、親しみやすく購買意欲を刺激する雰囲気を醸成。

- **Primary Color**: Deep Navy (oklch(0.25 0.05 240)) - 信頼性と品質を伝える主要ブランドカラー
- **Secondary Colors**: Warm Gray (oklch(0.85 0.02 60)) - コンテンツの背景とセクション分離
- **Accent Color**: Coral Orange (oklch(0.7 0.15 40)) - CTA ボタンと重要な要素のハイライト
- **Foreground/Background Pairings**: 
  - Background (Light Gray oklch(0.98 0.01 60)): Dark Navy text (oklch(0.2 0.05 240)) - Ratio 12.8:1 ✓
  - Primary (Deep Navy oklch(0.25 0.05 240)): White text (oklch(1 0 0)) - Ratio 8.2:1 ✓
  - Accent (Coral Orange oklch(0.7 0.15 40)): White text (oklch(1 0 0)) - Ratio 4.9:1 ✓

## Font Selection

クリーンで読みやすい Inter フォントを使用し、コンテンツの階層を明確にしながら現代的で洗練された印象を与える。

- **Typographic Hierarchy**: 
  - H1 (サイトロゴ): Inter Bold/24px/tight letter spacing
  - H2 (セクションタイトル): Inter Semibold/20px/normal letter spacing  
  - H3 (コンテンツタイトル): Inter Medium/16px/normal letter spacing
  - Body (説明文): Inter Regular/14px/relaxed line height

## Animations

控えめながらも意図的なアニメーションでユーザーの注意を自然に誘導し、プレミアムな体験を提供する。

- **Purposeful Meaning**: バナーのフェード切り替えでコンテンツの変化を滑らかに表現し、ホバー効果でインタラクティブ要素を明確化
- **Hierarchy of Movement**: バナーローテーション（最重要）→ カードホバーエフェクト（中程度）→ ボタンのマイクロインタラクション（控えめ）

## Component Selection

- **Components**: Header (カスタム)、Carousel (shadcn)、Card (shadcn)、Button (shadcn)、Badge (shadcn)、Separator (shadcn)
- **Customizations**: 自動ローテーション機能付きバナーカルーセル、商品グリッド用のレスポンシブカードレイアウト
- **States**: カードホバー時の軽いシャドウ効果、ボタンのpress状態でのスケール変化、画像ローディング時のスケルトン表示
- **Icon Selection**: Search (検索)、Heart (お気に入り)、ShoppingCart (カート)、Star (評価)、Tag (カテゴリ)
- **Spacing**: コンテナ間は space-y-8、カード間は gap-6、内部パディングは p-6使用
- **Mobile**: ヘッダーはハンバーガーメニュー化、バナーは高さ調整、グリッドは1列→2列→3列のレスポンシブ対応