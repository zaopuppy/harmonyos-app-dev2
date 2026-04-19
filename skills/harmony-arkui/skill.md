---
name: harmony-arkui
description: ArkUI 组件语法 - HarmonyOS 声明式 UI 框架
---

# ArkUI 组件参考

ArkUI 是 HarmonyOS 应用的声明式 UI 框架。

## 基础组件

### 内置组件

```typescript
// Text
Text('Hello World')
  .fontSize(24)
  .fontWeight(FontWeight.Bold)
  .fontColor('#333333')

// Image
Image($r('app.media.icon'))
  .width(100)
  .height(100)
  .objectFit(ImageFit.Cover)

// Button
Button('Click Me')
  .type(ButtonType.Capsule)
  .width(200)
  .height(48)
  .onClick(() => {
    console.info('Button clicked');
  })

// TextInput
TextInput({ placeholder: 'Enter text' })
  .width('100%')
  .height(48)
  .onChange((value: string) => {
    this.inputValue = value;
  })
```

### 布局容器

```typescript
// Column - 垂直布局
Column() {
  Text('Item 1')
  Text('Item 2')
  Text('Item 3')
}
.width('100%')
.alignItems(HorizontalAlign.Center)
.justifyContent(FlexAlign.SpaceBetween)

// Row - 水平布局
Row() {
  Image($r('app.media.avatar')).width(48).height(48)
  Text('Username').margin({ left: 12 })
  Blank()
  Image($r('app.media.arrow'))
}
.width('100%')
.padding(16)

// Stack - 叠加布局
Stack({ alignContent: Alignment.BottomEnd }) {
  Image($r('app.media.photo'))
  Badge({ count: 5 })
}

// Flex - 弹性布局
Flex({
  direction: FlexDirection.Row,
  wrap: FlexWrap.Wrap,
  justifyContent: FlexAlign.SpaceAround
}) {
  ForEach(this.items, (item: Item) => {
    ItemCard({ item: item })
  })
}
```

### 列表组件

```typescript
// 基础 List
List() {
  ForEach(this.dataList, (item: DataItem, index: number) => {
    ListItem() {
      Text(item.name)
    }
  }, (item: DataItem) => item.id)
}
.width('100%')
.divider({ strokeWidth: 1, color: '#E8E8E8' })

// 滑动操作
List() {
  ForEach(this.items, (item: Item) => {
    ListItem() {
      ItemRow({ item: item })
    }
    .swipeAction({
      end: this.DeleteButton(item.id)
    })
  })
}

@Builder
DeleteButton(id: string) {
  Button('Delete')
    .backgroundColor(Color.Red)
    .onClick(() => this.deleteItem(id))
}

// Grid
Grid() {
  ForEach(this.products, (product: Product) => {
    GridItem() {
      ProductCard({ product: product })
    }
  })
}
.columnsTemplate('1fr 1fr')
.rowsGap(12)
.columnsGap(12)

// WaterFlow (瀑布流布局)
WaterFlow() {
  ForEach(this.images, (image: ImageData) => {
    FlowItem() {
      Image(image.url)
        .width('100%')
        .aspectRatio(image.aspectRatio)
    }
  })
}
.columnsTemplate('1fr 1fr')
```

### 滚动组件

```typescript
// Scroll
Scroll() {
  Column() {
    ForEach(this.items, (item: Item) => {
      ItemCard({ item: item })
    })
  }
}
.scrollable(ScrollDirection.Vertical)
.scrollBar(BarState.Auto)
.edgeEffect(EdgeEffect.Spring)

// Swiper
Swiper() {
  ForEach(this.banners, (banner: Banner) => {
    Image(banner.imageUrl)
      .width('100%')
      .height(200)
  })
}
.autoPlay(true)
.interval(3000)
.indicator(true)

// Tabs
Tabs({ barPosition: BarPosition.Start }) {
  TabContent() {
    HomeTab()
  }.tabBar('Home')

  TabContent() {
    DiscoverTab()
  }.tabBar('Discover')

  TabContent() {
    ProfileTab()
  }.tabBar('Profile')
}
.barMode(BarMode.Fixed)
.onChange((index: number) => {
  this.currentTab = index;
})
```

## 自定义组件

### 基础结构

```typescript
@Component
struct UserCard {
  // 父组件传递的属性
  @Prop username: string = '';
  @Prop avatarUrl: string = '';

  // 本地状态
  @State isFollowing: boolean = false;

  build() {
    Row() {
      Image(this.avatarUrl)
        .width(48)
        .height(48)
        .borderRadius(24)

      Column() {
        Text(this.username)
          .fontSize(16)
          .fontWeight(FontWeight.Medium)
      }
      .margin({ left: 12 })
      .alignItems(HorizontalAlign.Start)

      Blank()

      Button(this.isFollowing ? 'Following' : 'Follow')
        .onClick(() => {
          this.isFollowing = !this.isFollowing;
        })
    }
    .width('100%')
    .padding(16)
  }
}
```

### @Builder 函数

```typescript
@Component
struct ProductList {
  @State products: Product[] = [];

  // 私有 builder
  @Builder
  ProductItem(product: Product) {
    Row() {
      Image(product.imageUrl)
        .width(80)
        .height(80)
      Column() {
        Text(product.name)
        Text(`$${product.price}`)
          .fontColor('#FF6B00')
      }
    }
  }

  // 带参数的 builder
  @Builder
  SectionHeader(title: string) {
    Text(title)
      .fontSize(18)
      .fontWeight(FontWeight.Bold)
      .margin({ top: 16, bottom: 8 })
  }

  build() {
    List() {
      ListItem() {
        this.SectionHeader('Featured Products')
      }

      ForEach(this.products, (product: Product) => {
        ListItem() {
          this.ProductItem(product)
        }
      })
    }
  }
}
```

### @BuilderParam (插槽)

```typescript
// 带插槽的 Card 组件
@Component
struct Card {
  @BuilderParam content: () => void = this.defaultContent;
  @BuilderParam footer: () => void = this.defaultFooter;

  @Builder
  defaultContent() {
    Text('Default content')
  }

  @Builder
  defaultFooter() {}

  build() {
    Column() {
      this.content()
      this.footer()
    }
    .padding(16)
    .backgroundColor(Color.White)
    .borderRadius(8)
  }
}

// 使用
@Component
struct ProductPage {
  build() {
    Card() {
      Column() {
        Image($r('app.media.product'))
        Text('Product Name')
      }
    }
    .footer(() => {
      Row() {
        Button('Add to Cart')
        Button('Buy Now')
      }
    })
  }
}
```

### @Styles 和 @Extend

```typescript
// 可复用样式
@Styles
function cardStyle() {
  .backgroundColor(Color.White)
  .borderRadius(12)
  .shadow({ radius: 8, color: '#1A000000' })
  .padding(16)
}

@Styles
function centerStyle() {
  .width('100%')
  .alignItems(HorizontalAlign.Center)
  .justifyContent(FlexAlign.Center)
}

// 扩展特定组件
@Extend(Text)
function titleStyle() {
  .fontSize(24)
  .fontWeight(FontWeight.Bold)
  .fontColor('#1A1A1A')
}

@Extend(Button)
function primaryButton() {
  .type(ButtonType.Capsule)
  .backgroundColor('#007AFF')
  .fontColor(Color.White)
  .width('100%')
  .height(48)
}

// 使用
@Component
struct StyledPage {
  build() {
    Column() {
      Column() {
        Text('Welcome')
          .titleStyle()
        Text('Description here')
      }
      .cardStyle()

      Button('Get Started')
        .primaryButton()
    }
    .centerStyle()
  }
}
```

## 动画

### 属性动画

```typescript
@Component
struct AnimatedButton {
  @State scale: number = 1;
  @State opacity: number = 1;

  build() {
    Button('Animated')
      .scale({ x: this.scale, y: this.scale })
      .opacity(this.opacity)
      .animation({
        duration: 300,
        curve: Curve.EaseInOut
      })
      .onTouch((event: TouchEvent) => {
        if (event.type === TouchType.Down) {
          this.scale = 0.95;
          this.opacity = 0.8;
        } else if (event.type === TouchType.Up) {
          this.scale = 1;
          this.opacity = 1;
        }
      })
  }
}
```

### 显式动画

```typescript
@Component
struct ExplicitAnimation {
  @State rotateAngle: number = 0;
  @State translateY: number = 0;

  build() {
    Column() {
      Image($r('app.media.icon'))
        .rotate({ angle: this.rotateAngle })
        .translate({ y: this.translateY })

      Button('Animate')
        .onClick(() => {
          animateTo({
            duration: 1000,
            curve: Curve.EaseInOut,
            iterations: 1,
            playMode: PlayMode.Normal
          }, () => {
            this.rotateAngle = 360;
            this.translateY = 100;
          })
        })
    }
  }
}
```

### 过渡动画

```typescript
@Component
struct TransitionDemo {
  @State isVisible: boolean = false;

  build() {
    Column() {
      Button('Toggle')
        .onClick(() => {
          this.isVisible = !this.isVisible;
        })

      if (this.isVisible) {
        Text('Animated Content')
          .transition({
            type: TransitionType.Insert,
            opacity: 0,
            translate: { y: 50 }
          })
          .transition({
            type: TransitionType.Delete,
            opacity: 0,
            scale: { x: 0.8, y: 0.8 }
          })
      }
    }
  }
}
```

## 手势

```typescript
@Component
struct GestureDemo {
  @State offsetX: number = 0;
  @State offsetY: number = 0;
  @State scale: number = 1;

  build() {
    Column() {
      Image($r('app.media.photo'))
        .translate({ x: this.offsetX, y: this.offsetY })
        .scale({ x: this.scale, y: this.scale })
        .gesture(
          PanGesture()
            .onActionUpdate((event: GestureEvent) => {
              this.offsetX = event.offsetX;
              this.offsetY = event.offsetY;
            })
        )
        .gesture(
          PinchGesture({ fingers: 2 })
            .onActionUpdate((event: GestureEvent) => {
              this.scale = event.scale;
            })
        )
        .gesture(
          GestureGroup(GestureMode.Parallel,
            TapGesture({ count: 2 })
              .onAction(() => {
                this.scale = this.scale === 1 ? 2 : 1;
              }),
            LongPressGesture()
              .onAction(() => {
                // 显示上下文菜单
              })
          )
        )
    }
  }
}
```

## 对话框和弹出框

```typescript
@Component
struct DialogDemo {
  dialogController: CustomDialogController = new CustomDialogController({
    builder: ConfirmDialog({
      title: 'Confirm',
      message: 'Are you sure?',
      onConfirm: () => this.handleConfirm(),
      onCancel: () => this.dialogController.close()
    }),
    autoCancel: true,
    alignment: DialogAlignment.Center
  });

  handleConfirm(): void {
    this.dialogController.close();
  }

  build() {
    Button('Show Dialog')
      .onClick(() => {
        this.dialogController.open();
      })
  }
}

@CustomDialog
struct ConfirmDialog {
  controller: CustomDialogController = new CustomDialogController({ builder: ConfirmDialog() });
  title: string = '';
  message: string = '';
  onConfirm: () => void = () => {};
  onCancel: () => void = () => {};

  build() {
    Column() {
      Text(this.title)
        .fontSize(18)
        .fontWeight(FontWeight.Bold)

      Text(this.message)
        .margin({ top: 16 })

      Row() {
        Button('Cancel')
          .onClick(() => this.onCancel())
        Button('Confirm')
          .onClick(() => this.onConfirm())
      }
      .margin({ top: 24 })
      .justifyContent(FlexAlign.SpaceEvenly)
      .width('100%')
    }
    .padding(24)
  }
}
```

## 响应式布局

```typescript
@Component
struct ResponsiveLayout {
  @StorageProp('currentBreakpoint') currentBreakpoint: string = 'sm';

  build() {
    GridRow({
      columns: { sm: 4, md: 8, lg: 12 },
      gutter: { x: 12, y: 12 }
    }) {
      GridCol({ span: { sm: 4, md: 4, lg: 3 } }) {
        this.Sidebar()
      }

      GridCol({ span: { sm: 4, md: 4, lg: 9 } }) {
        this.MainContent()
      }
    }
  }

  @Builder
  Sidebar() {
    Column() {
      // Sidebar content
    }
    .visibility(this.currentBreakpoint === 'sm'
      ? Visibility.None
      : Visibility.Visible)
  }

  @Builder
  MainContent() {
    Column() {
      // Main content
    }
  }
}
```

## 最佳实践

### 组件设计

```typescript
// ✅ 好：单一职责，可复用
@Component
struct Avatar {
  @Prop src: string = '';
  @Prop size: number = 48;
  @Prop borderRadius: number = 24;

  build() {
    Image(this.src)
      .width(this.size)
      .height(this.size)
      .borderRadius(this.borderRadius)
      .objectFit(ImageFit.Cover)
  }
}

// ✅ 好：组合优于继承
@Component
struct UserProfile {
  @Prop user: User = new User();

  build() {
    Row() {
      Avatar({ src: this.user.avatar, size: 64 })
      Column() {
        Text(this.user.name)
        Text(this.user.bio)
      }
    }
  }
}
```

### 性能

```typescript
// ✅ 好：大列表使用 LazyForEach
LazyForEach(this.dataSource, (item: Item) => {
  ListItem() {
    ItemCard({ item: item })
  }
}, (item: Item) => item.id)

// ✅ 好：为 ForEach 提供 key 函数
ForEach(this.items, (item: Item, index: number) => {
  ItemRow({ item: item })
}, (item: Item) => item.id)

// ✅ 好：避免不必要的重渲染
@Component
struct OptimizedList {
  @State @Watch('onDataChange') items: Item[] = [];

  onDataChange(): void {
    // 仅在 items 实际变化时调用
  }
}
```
