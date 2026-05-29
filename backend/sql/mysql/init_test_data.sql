insert into sys_dept (id, name, sort, leader, phone, email, status, deleted, parent_id, created_time, updated_time)
values (1, '测试', 0, null, null, null, 1, 0, null, now(), null);

insert into sys_menu (id, title, name, path, sort, icon, type, component, perms, status, display, cache, link, remark, parent_id, created_time, updated_time)
values
(1, 'page.dashboard.title', 'Dashboard', '/dashboard', 0, 'ant-design:dashboard-outlined', 0, null, null, 1, 1, 1, '', null, null, '2025-06-26 20:29:06', null),
(2, 'page.dashboard.analytics', 'Analytics', '/analytics', 0, 'lucide:area-chart', 1, '/dashboard/analytics/index', null, 1, 1, 1, '', null, 1, '2025-06-26 20:29:06', null),
(3, 'page.dashboard.workspace', 'Workspace', '/workspace', 1, 'carbon:workspace', 1, '/dashboard/workspace/index', null, 1, 1, 1, '', null, 1, '2025-06-26 20:29:06', null),
(4, 'page.menu.system', 'System', '/system', 1, 'eos-icons:admin', 0, null, null, 1, 1, 1, '', null, null, '2025-06-26 20:29:06', null),
(5, 'page.menu.sysDept', 'SysDept', '/system/dept', 1, 'mingcute:department-line', 1, '/system/dept/index', null, 1, 1, 1, '', null, 4, '2025-06-26 20:29:06', null),
(6, '新增', 'AddSysDept', null, 0, null, 2, null, 'sys:dept:add', 1, 0, 1, '', null, 5, '2025-06-26 20:29:06', null),
(7, '修改', 'EditSysDept', null, 0, null, 2, null, 'sys:dept:edit', 1, 0, 1, '', null, 5, '2025-06-26 20:29:06', null),
(8, '删除', 'DeleteSysDept', null, 0, null, 2, null, 'sys:dept:del', 1, 0, 1, '', null, 5, '2025-06-26 20:29:06', null),
(9, 'page.menu.sysUser', 'SysUser', '/system/user', 2, 'ant-design:user-outlined', 1, '/system/user/index', null, 1, 1, 1, '', null, 4, '2025-06-26 20:29:06', null),
(10, '删除', 'DeleteSysUser', null, 0, null, 2, null, 'sys:user:del', 1, 0, 1, '', null, 9, '2025-06-26 20:29:06', null),
(11, 'page.menu.sysRole', 'SysRole', '/system/role', 3, 'carbon:user-role', 1, '/system/role/index', null, 1, 1, 1, '', null, 4, '2025-06-26 20:29:06', null),
(12, '新增', 'AddSysRole', null, 0, null, 2, null, 'sys:role:add', 1, 0, 1, '', null, 11, '2025-06-26 20:29:06', null),
(13, '修改', 'EditSysRole', null, 0, null, 2, null, 'sys:role:edit', 1, 0, 1, '', null, 11, '2025-06-26 20:29:06', null),
(14, '修改角色菜单', 'EditSysRoleMenu', null, 0, null, 2, null, 'sys:role:menu:edit', 1, 0, 1, '', null, 11, '2025-06-26 20:29:06', null),
(15, '修改角色数据范围', 'EditSysRoleScope', null, 0, null, 2, null, 'sys:role:scope:edit', 1, 0, 1, '', null, 11, '2025-06-26 20:29:06', null),
(16, '删除', 'DeleteSysRole', null, 0, null, 2, null, 'sys:role:del', 1, 0, 1, '', null, 11, '2025-06-26 20:29:06', null),
(17, 'page.menu.sysMenu', 'SysMenu', '/system/menu', 4, 'ant-design:menu-outlined', 1, '/system/menu/index', null, 1, 1, 1, '', null, 4, '2025-06-26 20:29:06', null),
(18, '新增', 'AddSysMenu', null, 0, null, 2, null, 'sys:menu:add', 1, 0, 1, '', null, 17, '2025-06-26 20:29:06', null),
(19, '修改', 'EditSysMenu', null, 0, null, 2, null, 'sys:menu:edit', 1, 0, 1, '', null, 17, '2025-06-26 20:29:06', null),
(20, '删除', 'DeleteSysMenu', null, 0, null, 2, null, 'sys:menu:del', 1, 0, 1, '', null, 17, '2025-06-26 20:29:06', null),
(21, 'page.menu.sysDataPermission', 'SysDataPermission', '/system/data-permission', 5, 'icon-park-outline:permissions', 0, null, null, 1, 1, 1, '', null, 4, '2025-06-26 20:29:06', null),
(22, 'page.menu.sysDataScope', 'SysDataScope', '/system/data-scope', 6, 'cuida:scope-outline', 1, '/system/data-permission/scope/index', null, 1, 1, 1, '', null, 21, '2025-06-26 20:29:06', '2025-06-26 20:37:26'),
(23, '新增', 'AddSysDataScope', null, 0, null, 2, null, 'data:scope:add', 1, 0, 1, '', null, 22, '2025-06-26 20:29:06', null),
(24, '修改', 'EditSysDataScope', null, 0, null, 2, null, 'data:scope:edit', 1, 0, 1, '', null, 22, '2025-06-26 20:29:06', null),
(25, '修改数据范围规则', 'EditDataScopeRule', null, 0, null, 2, null, 'data:scope:rule:edit', 1, 0, 1, '', null, 22, '2025-06-26 20:29:06', null),
(26, '删除', 'DeleteSysDataScope', null, 0, null, 2, null, 'data:scope:del', 1, 0, 1, '', null, 22, '2025-06-26 20:29:06', null),
(27, 'page.menu.sysDataRule', 'SysDataRule', '/system/data-rule', 7, 'material-symbols:rule', 1, '/system/data-permission/rule/index', null, 1, 1, 1, '', null, 21, '2025-06-26 20:29:06', '2025-06-26 20:37:40'),
(28, '新增', 'AddSysDataRule', null, 0, null, 2, null, 'data:rule:add', 1, 0, 1, '', null, 27, '2025-06-26 20:29:06', null),
(29, '修改', 'EditSysDataRule', null, 0, null, 2, null, 'data:rule:edit', 1, 0, 1, '', null, 27, '2025-06-26 20:29:06', null),
(30, '删除', 'DeleteSysDataRule', null, 0, null, 2, null, 'data:rule:del', 1, 0, 1, '', null, 27, '2025-06-26 20:29:06', null),
(31, 'page.menu.sysPlugin', 'SysPlugin', '/system/plugin', 8, 'clarity:plugin-line', 1, '/system/plugin/index', null, 1, 1, 1, '', null, 4, '2025-06-26 20:29:06', null),
(32, 'page.menu.scheduler', 'Scheduler', '/scheduler', 2, 'material-symbols:automation', 0, null, null, 1, 1, 1, '', null, null, '2025-06-26 20:29:06', null),
(33, 'page.menu.schedulerManage', 'SchedulerManage', '/scheduler/manage', 1, 'ix:scheduler', 1, '/scheduler/manage/index', null, 1, 1, 1, '', null, 32, '2025-06-26 20:29:06', null),
(34, 'page.menu.schedulerRecord', 'SchedulerRecord', '/scheduler/record', 2, 'ix:scheduler', 1, '/scheduler/record/index', null, 1, 1, 1, '', null, 32, '2025-06-26 20:29:06', null),
(35, 'page.menu.log', 'Log', '/log', 3, 'carbon:cloud-logging', 0, null, null, 1, 1, 1, '', null, null, '2025-06-26 20:29:06', null),
(36, 'page.menu.login', 'LoginLog', '/log/login', 1, 'mdi:login', 1, '/log/login/index', null, 1, 1, 1, '', null, 35, '2025-06-26 20:29:06', null),
(37, '删除', 'DeleteLoginLog', null, 0, null, 2, null, 'log:login:del', 1, 0, 1, '', null, 36, '2025-06-26 20:29:06', null),
(38, '清空', 'EmptyLoginLog', null, 0, null, 2, null, 'log:login:clear', 1, 0, 1, '', null, 36, '2025-06-26 20:29:06', null),
(39, 'page.menu.opera', 'OperaLog', '/log/opera', 2, 'carbon:operations-record', 1, '/log/opera/index', null, 1, 1, 1, '', null, 35, '2025-06-26 20:29:06', null),
(40, '删除', 'DeleteOperaLog', null, 0, null, 2, null, 'log:opera:del', 1, 0, 1, '', null, 39, '2025-06-26 20:29:06', null),
(41, '清空', 'EmptyOperaLog', null, 0, null, 2, null, 'log:opera:clear', 1, 0, 1, '', null, 39, '2025-06-26 20:29:06', null),
(42, 'page.menu.monitor', 'Monitor', '/monitor', 4, 'mdi:monitor-eye', 0, null, null, 1, 1, 1, '', null, null, '2025-06-26 20:29:06', null),
(43, 'page.menu.online', 'Online', '/log/online', 1, 'wpf:online', 1, '/monitor/online/index', null, 1, 1, 1, '', null, 42, '2025-06-26 20:29:06', null),
(44, 'page.menu.redis', 'Redis', '/monitor/redis', 2, 'devicon:redis', 1, '/monitor/redis/index', null, 1, 1, 1, '', null, 42, '2025-06-26 20:29:06', null),
(45, 'page.menu.server', 'Server', '/monitor/server', 3, 'mdi:server-outline', 1, '/monitor/server/index', null, 1, 1, 1, '', null, 42, '2025-06-26 20:29:06', null),
(46, '项目', 'Project', '/fba', 5, 'https://wu-clan.github.io/picx-images-hosting/logo/fba.png', 0, null, null, 1, 1, 1, '', null, null, '2025-06-26 20:29:06', null),
(47, '文档', 'Document', '/fba/document', 1, 'lucide:book-open-text', 4, '/_core/fallback/iframe.vue', null, 1, 1, 1, 'https://fastapi-practices.github.io/fastapi_best_architecture_docs', null, 46, '2025-06-26 20:29:06', null),
(48, 'Github', 'Github', '/fba/github', 2, 'ant-design:github-filled', 4, '/_core/fallback/iframe.vue', null, 1, 1, 1, 'https://github.com/fastapi-practices/fastapi-best-architecture', null, 46, '2025-06-26 20:29:06', null),
(49, 'Apifox', 'Apifox', '/fba/apifox', 3, 'simple-icons:apifox', 3, '/_core/fallback/iframe.vue', null, 1, 1, 1, 'https://apifox.com/apidoc/shared-28a93f02-730b-4f33-bb5e-4dad92058cc0', null, 46, '2025-06-26 20:29:06', null),
(50, 'page.menu.profile', 'Profile', '/profile', 6, 'ant-design:profile-outlined', 1, '/_core/profile/index', null, 1, 0, 1, '', null, null, '2025-06-26 20:29:06', null);

insert into sys_role (id, name, status, is_filter_scopes, remark, created_time, updated_time)
values (1, '测试', 1, true, null, now(), null);

insert into sys_role_menu (id, role_id, menu_id)
values
(1, 1, 1),
(2, 1, 2),
(3, 1, 3),
(4, 1, 50);

insert into sys_user (id, uuid, username, nickname, password, salt, email, status, is_superuser, is_staff, is_multi_login, avatar, phone, join_time, last_login_time, last_password_changed_time, dept_id, created_time, updated_time)
values
(1, uuid(), 'admin', '用户88888', '$2b$12$8y2eNucX19VjmZ3tYhBLcOsBwy9w1IjBQE4SSqwMDL5bGQVp2wqS.', unhex('24326224313224387932654E7563583139566A6D5A33745968424C634F'), 'admin@example.com', 1, true, true, true, null, null, now(), now(), now(), 1, now(), null),
(2, uuid(), 'test', '用户66666', '$2b$12$BMiXsNQAgTx7aNc7kVgnwedXGyUxPEHRnJMFbiikbqHgVoT3y14Za', unhex('24326224313224424D6958734E514167547837614E63376B56676E7765'), 'test@example.com', 1, false, false, false, null, null, now(), now(), now(), 1, now(), null);

insert into sys_user_role (id, user_id, role_id)
values
(1, 1, 1),
(2, 2, 1);

insert into sys_data_scope (id, name, status, created_time, updated_time)
values
(1, '本部门数据权限', 1, now(), null),
(2, '部门及以下数据权限', 1, now(), null),
(3, '仅本人数据权限', 1, now(), null),
(4, '全模型本部门数据权限', 1, now(), null),
(5, '排除超级管理员数据权限', 1, now(), null);

insert into sys_data_rule (id, name, model, `column`, operator, expression, `value`, created_time, updated_time)
values
(1, '部门 ID 等于当前用户部门', 'Dept', '__dept_id__', 0, 0, '${dept_id}', now(), null),
(2, '部门名称等于测试', 'Dept', 'name', 1, 0, '测试', now(), null),
(3, '父部门 ID 等于测试部门 ID', 'Dept', 'parent_id', 0, 0, '1', now(), null),
(4, '创建者等于当前用户', '__ALL__', '__created_by__', 0, 0, '${user_id}', now(), null),
(5, '全模型部门 ID 等于当前用户部门', '__ALL__', '__dept_id__', 0, 0, '${dept_id}', now(), null),
(6, '用户非超级管理员', 'User', 'is_superuser', 0, 1, '1', now(), null);

insert into sys_role_data_scope (id, role_id, data_scope_id)
values
(1, 1, 1),
(2, 1, 2);

insert into sys_data_scope_rule (id, data_scope_id, data_rule_id)
values
(1, 1, 1),
(2, 2, 2),
(3, 2, 3),
(4, 3, 4),
(5, 4, 5),
(6, 5, 6);
