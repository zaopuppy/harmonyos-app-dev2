---
name: harmony-ut
description: HarmonyOS 单元测试
---

# HarmonyOS 单元测试参考

提供 HarmonyOS 应用单元测试的框架和实践参考。

## 测试框架

- Hypium (内置测试框架) — 推荐使用
- Vitest
- Jest

## 测试类型

- 单元测试
- 集成测试
- UI 测试

## 单元测试

```typescript
import { describe, it, expect, beforeEach } from '@ohos/hypium';
import { ProductViewModel } from '../viewmodel/ProductViewModel';

export default function ProductViewModelTest() {
  describe('ProductViewModel', () => {
    let viewModel: ProductViewModel;

    beforeEach(() => {
      viewModel = new ProductViewModel();
    });

    it('should load products successfully', async () => {
      await viewModel.loadProducts();

      expect(viewModel.products.length).assertLarger(0);
      expect(viewModel.isLoading).assertFalse();
      expect(viewModel.errorMessage).assertEqual('');
    });

    it('should add product to list', async () => {
      const initialCount = viewModel.products.length;
      const newProduct: Product = { id: 'test', name: 'Test Product', price: 99 };

      await viewModel.addProduct(newProduct);

      expect(viewModel.products.length).assertEqual(initialCount + 1);
    });
  });
}
```

## UI 测试

```typescript
import { describe, it, expect } from '@ohos/hypium';
import { Driver, ON } from '@ohos.UiTest';

export default function ProductPageUITest() {
  describe('ProductPage UI', () => {
    it('should display product list', async () => {
      const driver = Driver.create();
      await driver.delayMs(1000);

      // Find and verify list exists
      const list = await driver.findComponent(ON.type('List'));
      expect(list).not().assertNull();

      // Verify list items
      const items = await driver.findComponents(ON.type('ListItem'));
      expect(items.length).assertLarger(0);
    });

    it('should navigate to detail on tap', async () => {
      const driver = Driver.create();

      // Find first product card
      const card = await driver.findComponent(ON.type('ProductCard'));
      await card.click();

      await driver.delayMs(500);

      // Verify navigation to detail page
      const detailTitle = await driver.findComponent(ON.text('Product Detail'));
      expect(detailTitle).not().assertNull();
    });
  });
}
```

## 实践

### Mock 技巧

```typescript
import mock from '@ohos.mock';

mock.mockValue('http.createHttp', () => {
  return {
    request: (url: string, options: Object) => {
      return {
        result: JSON.stringify({ code: 0, data: mockData }),
        responseCode: 200
      };
    },
    destroy: () => {}
  };
});
```

### 异步测试

```typescript
it('should handle async operations', async () => {
  const result = await asyncOperation();
  expect(result).assertEqual(expectedValue);
});
```

### 覆盖率

使用 ArkUI 内置的覆盖率工具生成覆盖率报告。

### 测试用例编写规范

1. **AAA 模式** — Arrange (准备), Act (执行), Assert (断言)
2. **单一职责** — 每个测试用例只验证一个行为
3. **清晰的测试名称** — 名称应描述预期行为
4. **独立性** — 测试用例之间无依赖
