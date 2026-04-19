---
name: harmony-arkts
description: ArkTS 语法参考 - HarmonyOS 应用开发语言
---

# ArkTS 语法参考

ArkTS 是 TypeScript 的超集，专为 HarmonyOS 优化，支持静态类型检查和 UI 声明扩展。

## 核心原则

- **严格类型** — 禁用 `any`，禁止动态类型
- **不可变更新** — 状态修改必须创建新对象
- **完整类型标注** — 显式声明所有类型

## 禁止的模式

```typescript
// ❌ 禁止：动态类型
let data: any = fetchData();
let obj: object = {};
obj['dynamicKey'] = value;
(someVar as SomeType).method();

// ✅ 要求：严格类型
interface UserData {
  id: string;
  name: string;
}
let data: UserData = fetchData();
let obj: Record<string, string> = {};
obj['key'] = value;
```

```typescript
// ❌ 禁止：直接修改状态
@State user: User = { name: 'John', age: 25 };
this.user.age = 26;  // UI 不会更新！

// ✅ 要求：不可变更新
this.user = { ...this.user, age: 26 };
```

## TypeScript vs ArkTS 差异

### 禁止的特性

```typescript
// 以下 TypeScript 特性在 ArkTS 中不允许

// 1. any 类型
let data: any;  // 错误！

// 2. unknown 类型断言
let value: unknown;
(value as string).length;  // 错误！

// 3. 动态属性访问
let obj = {};
obj['key'] = value;  // 错误！（除非使用 Record）

// 4. 结构化类型（类必须有继承关系）
class A { x: number = 0; }
class B { x: number = 0; }
let a: A = new B();  // 错误！类必须显式相关

// 5. typeof 用于类型
type T = typeof someVariable;  // 错误！

// 6. keyof 操作符
type Keys = keyof SomeType;  // 错误！

// 7. 条件类型
type Check<T> = T extends string ? 'yes' : 'no';  // 错误！
```

### 允许的模式

```typescript
// ✅ 允许的模式

// 1. 显式类型
let data: string = 'hello';
let count: number = 42;

// 2. 接口
interface User {
  id: string;
  name: string;
  age?: number;
}

// 3. 类型别名（基础）
type UserId = string;
type Callback = (data: string) => void;

// 4. 泛型（基础）
class Container<T> {
  private value: T;
  constructor(value: T) {
    this.value = value;
  }
  getValue(): T {
    return this.value;
  }
}

// 5. Record 类型用于动态键
let map: Record<string, number> = {};
map['key1'] = 100;  // OK

// 6. 枚举
enum Color {
  Red,
  Green,
  Blue
}

// 7. 类继承
class Animal {
  name: string = '';
}
class Dog extends Animal {
  breed: string = '';
}
```

## 类型系统

### 基础类型

```typescript
// 数值
let integer: number = 42;
let float: number = 3.14;

// 字符串
let text: string = 'Hello';
let template: string = `Value: ${integer}`;

// 布尔
let flag: boolean = true;

// 数组
let numbers: number[] = [1, 2, 3];
let strings: Array<string> = ['a', 'b', 'c'];

// 元组
let tuple: [string, number] = ['age', 25];

// Null 和 undefined
let nullable: string | null = null;
let optional: string | undefined = undefined;
```

### 对象类型

```typescript
// 接口
interface Product {
  readonly id: string;
  name: string;
  price: number;
  description?: string;
}

// 类型别名
type Point = {
  x: number;
  y: number;
};
```

### 函数类型

```typescript
// 函数声明
function add(a: number, b: number): number {
  return a + b;
}

// 箭头函数
const multiply = (a: number, b: number): number => a * b;

// 可选参数
function greet(name: string, greeting?: string): string {
  return `${greeting ?? 'Hello'}, ${name}`;
}

// 默认参数
function createUser(name: string, role: string = 'user'): User {
  return { name, role };
}

// 回调类型
type ClickHandler = (event: ClickEvent) => void;
```

### 泛型

```typescript
// 泛型函数
function identity<T>(value: T): T {
  return value;
}

// 泛型接口
interface Repository<T> {
  getById(id: string): Promise<T>;
  save(item: T): Promise<void>;
}

// 泛型约束
interface HasId {
  id: string;
}

class EntityRepository<T extends HasId> {
  save(entity: T): void {
    this.entities.set(entity.id, entity);
  }
}
```

## 类

### 类声明

```typescript
class User {
  private id: string = '';
  public name: string = '';
  protected email: string = '';
  readonly createdAt: Date = new Date();

  static userCount: number = 0;

  constructor(id: string, name: string, email: string) {
    this.id = id;
    this.name = name;
    this.email = email;
    User.userCount++;
  }

  public getDisplayName(): string {
    return this.name;
  }

  get displayId(): string {
    return `USER-${this.id}`;
  }

  set displayId(value: string) {
    this.id = value.replace('USER-', '');
  }

  static createGuest(): User {
    return new User('guest', 'Guest', 'guest@example.com');
  }
}
```

### 继承

```typescript
abstract class Shape {
  abstract area(): number;

  describe(): string {
    return `Area: ${this.area()}`;
  }
}

class Rectangle extends Shape {
  constructor(private width: number, private height: number) {
    super();
  }

  area(): number {
    return this.width * this.height;
  }
}

interface Drawable {
  draw(): void;
}

class Circle extends Shape implements Drawable {
  constructor(private radius: number) {
    super();
  }

  area(): number {
    return Math.PI * this.radius ** 2;
  }

  draw(): void {
    console.info(`Drawing circle with radius ${this.radius}`);
  }
}
```

## 异步编程

```typescript
// 异步函数
async function fetchUser(id: string): Promise<User> {
  const response = await httpClient.get<User>(`/users/${id}`);
  return response;
}

// 错误处理
async function safeGetUser(id: string): Promise<User | null> {
  try {
    return await fetchUser(id);
  } catch (error) {
    console.error(`Failed: ${(error as Error).message}`);
    return null;
  }
}

// 并行执行
async function loadDashboard(): Promise<DashboardData> {
  const [user, orders] = await Promise.all([
    fetchUser('current'),
    fetchOrders()
  ]);
  return { user, orders };
}
```

## 模块系统

```typescript
// 命名导出
export function add(a: number, b: number): number {
  return a + b;
}

export const PI = 3.14159;

// 默认导出
export default class User {
  constructor(public name: string) {}
}

// 命名导入
import { add, PI } from '../utils/math';

// 默认导入
import User from '../models/User';

// 重命名导入
import { add as sum } from '../utils/math';

// 重新导出
export { add, multiply } from './math';
```

## 最佳实践

1. **始终初始化属性**
   ```typescript
   class User {
     name: string = '';  // 必须初始化
   }
   ```

2. **使用显式返回类型**
   ```typescript
   function getUser(id: string): User {
     return { id, name: 'John' };
   }
   ```

3. **对象类型优先使用接口**
   ```typescript
   interface User {
     id: string;
     name: string;
   }
   ```

4. **动态键使用 Record**
   ```typescript
   let cache: Record<string, CacheEntry> = {};
   cache['key'] = value;  // OK
   ```

5. **避免不必要的可选链**
   ```typescript
   const user: User = getUser();
   console.log(user.name);  // user 不可空时不用 ?
   ```
