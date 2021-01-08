使用mocha 对`ts`进行单元测试的时候，如果使用了  `.d.ts`文件 或者使用全局`namesapce`定义，会出现类似 找不到 namespace的定义。
问题的根本原因是 mocha 的 `--require ts-node/register`  时, ts-node 不会加载 `.d.ts`文件，解决办法如下：

修改 `tsconfig.json`
```
{
 "ts-node":{
	"files":true,
 },
 "compilerOptions":{
 xxxx
    "include":[".d.ts所在的文件夹"]
 }

}
```
