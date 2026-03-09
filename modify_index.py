import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. State Injection
state_injection = '''                    return [];
                });

                const [activeMenu, setActiveMenu] = React.useState('1');

                const [propTradingData, setPropTradingData] = React.useState(() => {
                    const saved = localStorage.getItem('edgy_prop_trading');
                    if (saved) {
                        try { return JSON.parse(saved); } catch (e) { return []; }
                    }
                    return [
                        { id: '1', name: 'Tradeify PA #1', firm: 'Tradeify', balance: 50000.00, pnlDiario: 850.00, goal: 3000.00, type: 'Evaluación Fase 1' }
                    ];
                });

                React.useEffect(() => {
                    localStorage.setItem('edgy_prop_trading', JSON.stringify(propTradingData));
                }, [propTradingData]);

                const [isPropModalVisible, setIsPropModalVisible] = React.useState(false);
                const [propForm] = Form.useForm();

                const getProgressPercent = (balanceNew, balanceInitial, goal) => {
                    if (!goal) return 0;
                    if (balanceNew === balanceInitial) return 0;
                    const percent = ((balanceNew - balanceInitial) / goal) * 100;
                    return parseFloat(percent.toFixed(1));
                };

                const getProgressColor = (percent) => {
                    if (percent >= 100) return '#00b96b';
                    if (percent >= 80) return '#1677ff';
                    if (percent >= 50) return '#faad14';
                    return '#ff4d4f';
                };

                const handlePropSubmit = (values) => {
                    const newAcc = { ...values, id: Date.now().toString() };
                    setPropTradingData([...propTradingData, newAcc]);
                    setIsPropModalVisible(false);
                    propForm.resetFields();
                    message.success('Cuenta Prop agregada con éxito.');
                };

                const handleDeleteProp = (id) => {
                    setPropTradingData(propTradingData.filter(a => a.id !== id));
                    message.success('Cuenta Prop eliminada.');
                };

                React.useEffect(() => {'''
content = content.replace('''                    return [];
                });

                React.useEffect(() => {''', state_injection)

# 2. Menu update
menu_current = '''                                <Menu
                                    theme="dark"
                                    style={{ background: PRIMARY_COLOR }}
                                    mode="inline"
                                    defaultSelectedKeys={['1']}
                                    items={[
                                        { key: '1', icon: DashboardOutlined && <DashboardOutlined />, label: 'Dashboard' },
                                        { key: '2', icon: LineChartOutlined && <LineChartOutlined />, label: 'Análisis de Trading' },
                                        { key: '3', icon: BankOutlined && <BankOutlined />, label: 'Cuentas' },
                                        { key: '4', icon: WalletOutlined && <WalletOutlined />, label: 'Retiros' },
                                        { type: 'divider' },
                                        { key: 'logout', icon: LogoutOutlined && <LogoutOutlined />, label: 'Cerrar Sesión', danger: true }
                                    ]}
                                    onClick={({ key }) => {
                                        if (key === 'logout') {
                                            setIsAuthenticated(false);
                                            message.info('Sesión cerrada.');
                                        }
                                    }}
                                />'''
menu_new = '''                                <Menu
                                    theme="dark"
                                    style={{ background: PRIMARY_COLOR }}
                                    mode="inline"
                                    selectedKeys={[activeMenu]}
                                    items={[
                                        { key: '1', icon: DashboardOutlined && <DashboardOutlined />, label: 'Dashboard' },
                                        { key: 'prop_trading', icon: DashboardOutlined && <DashboardOutlined />, label: 'Prop Trading' },
                                        { key: '2', icon: LineChartOutlined && <LineChartOutlined />, label: 'Análisis de Trading' },
                                        { key: '3', icon: BankOutlined && <BankOutlined />, label: 'Cuentas' },
                                        { key: '4', icon: WalletOutlined && <WalletOutlined />, label: 'Retiros' },
                                        { type: 'divider' },
                                        { key: 'logout', icon: LogoutOutlined && <LogoutOutlined />, label: 'Cerrar Sesión', danger: true }
                                    ]}
                                    onClick={({ key }) => {
                                        if (key === 'logout') {
                                            setIsAuthenticated(false);
                                            message.info('Sesión cerrada.');
                                        } else {
                                            setActiveMenu(key);
                                        }
                                    }}
                                />'''
if menu_current in content:
    content = content.replace(menu_current, menu_new)
else:
    print('Error: Could not find Menu section to replace.')

# 3. Content div wrappers
content_start = '''<Content style={{ margin: '24px 24px', overflow: 'initial' }}>
                                    <div style={{ marginBottom: 24 }}>'''
content_start_new = '''<Content style={{ margin: '24px 24px', overflow: 'initial' }}>
                                  <div style={{ display: activeMenu === '1' ? 'block' : 'none' }}>
                                    <div style={{ marginBottom: 24 }}>'''
content = content.replace(content_start, content_start_new)

content_end = '''                                        </Card>
                                    )}
                                </Content>'''
content_end_new = '''                                        </Card>
                                    )}
                                  </div>

                                  <div style={{ display: activeMenu === 'prop_trading' ? 'block' : 'none' }}>
                                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
                                          <div>
                                              <Title level={2} style={{ marginBottom: 4 }}>Módulo de Prop Trading</Title>
                                              <Text type="secondary" style={{ fontSize: 16 }}>Monitoreo de evaluaciones y cuentas reales.</Text>
                                          </div>
                                          <Button type="primary" icon={<PlusOutlined />} onClick={() => setIsPropModalVisible(true)}>
                                              Nueva Cuenta Prop Trading
                                          </Button>
                                      </div>

                                      {[
                                        { title: 'Evaluación Fase 1', type: 'Evaluación Fase 1', color: '#1677ff' },
                                        { title: 'Evaluación Fase 2', type: 'Evaluación Fase 2', color: '#722ed1' },
                                        { title: 'Real', type: 'Real', color: '#52c41a' }
                                      ].map(section => {
                                          const sectionData = propTradingData.filter(item => item.type === section.type);
                                          if (sectionData.length === 0) return null;
                                          return (
                                              <Card key={section.type} title={<span style={{ fontSize: 18, color: section.color }}>{section.title}</span>} className="premium-card" style={{ marginBottom: 24 }}>
                                                  <Table
                                                      dataSource={sectionData}
                                                      pagination={false}
                                                      rowKey="id"
                                                      columns={[
                                                          { title: 'Compañía', dataIndex: 'firm', key: 'firm' },
                                                          { title: 'Nombre', dataIndex: 'name', key: 'name', render: (text) => <strong>{text}</strong> },
                                                          { title: 'Balance Inicial', dataIndex: 'balance', key: 'balance', render: val => `$ ${val.toLocaleString()}` },
                                                          { title: 'P&L Diario', dataIndex: 'pnlDiario', key: 'pnlDiario', render: val => <span style={{ color: val >= 0 ? '#3f8600' : '#cf1322', fontWeight: 600 }}>{val >= 0 ? '+' : '-'}${Math.abs(val).toLocaleString()}</span> },
                                                          { title: 'Balance New', key: 'newBal', render: (_, record) => { const bal = record.balance + record.pnlDiario; return <strong>$ {bal.toLocaleString()}</strong> } },
                                                          { title: 'Meta / Retiro', dataIndex: 'goal', key: 'goal', render: val => val ? `$ ${val.toLocaleString()}` : '-' },
                                                          { title: 'Progreso', key: 'prog', render: (_, record) => {
                                                              let percent = getProgressPercent(record.balance + record.pnlDiario, record.balance, record.goal);
                                                              const exactPercent = percent.toFixed(1);
                                                              let percentUI = percent < 0 ? 0 : (percent > 100 ? 100 : percent);
                                                              return (
                                                                  <div style={{ width: 140 }}>
                                                                    <Progress percent={percentUI} format={() => `${exactPercent}%`} status={record.pnlDiario < 0 ? 'exception' : 'active'} strokeColor={record.pnlDiario >= 0 ? getProgressColor(percent) : undefined} />
                                                                  </div>
                                                              );
                                                          }},
                                                          { title: 'Acción', key: 'action', render: (_, record) => <Button type="text" danger icon={<DeleteOutlined />} onClick={() => handleDeleteProp(record.id)} /> }
                                                      ]}
                                                  />
                                              </Card>
                                          );
                                      })}
                                  </div>
                                </Content>'''
if content_end in content:
    content = content.replace(content_end, content_end_new)
else:
    print('Error: Could not find Content end to replace.')

# 4. Modals append
modal_current = '''                            </Form>
                        </Modal>

                    </ConfigProvider>'''
modal_new = '''                            </Form>
                        </Modal>

                        {/* Modal Prop Trading */}
                        <Modal title="Nueva Cuenta Prop Trading" open={isPropModalVisible} onCancel={() => { setIsPropModalVisible(false); propForm.resetFields(); }} onOk={() => propForm.submit()} okText="Guardar" cancelText="Cancelar">
                            <Form form={propForm} layout="vertical" onFinish={handlePropSubmit}>
                                <Row gutter={16}>
                                    <Col span={12}>
                                        <Form.Item name="firm" label="Compañía" rules={[{ required: true, message: 'Requerido' }]}>
                                            <Input placeholder="Ej. Tradeify, Topstep" />
                                        </Form.Item>
                                    </Col>
                                    <Col span={12}>
                                        <Form.Item name="name" label="Nombre" rules={[{ required: true, message: 'Requerido' }]}>
                                            <Input placeholder="Ej. Tradeify PA #1" />
                                        </Form.Item>
                                    </Col>
                                </Row>
                                <Form.Item name="type" label="Tipo" rules={[{ required: true, message: 'Requerido' }]}>
                                    <Select placeholder="Seleccione el tipo">
                                        <Select.Option value="Evaluación Fase 1">Evaluación Fase 1</Select.Option>
                                        <Select.Option value="Evaluación Fase 2">Evaluación Fase 2</Select.Option>
                                        <Select.Option value="Real">Real</Select.Option>
                                    </Select>
                                </Form.Item>
                                <Row gutter={16}>
                                    <Col span={8}>
                                        <Form.Item name="balance" label="Balance Inicial" rules={[{ required: true, message: 'Requerido' }]}>
                                            <InputNumber style={{ width: '100%' }} />
                                        </Form.Item>
                                    </Col>
                                    <Col span={8}>
                                        <Form.Item name="pnlDiario" label="PNL Diario" rules={[{ required: true, message: 'Requerido' }]}>
                                            <InputNumber style={{ width: '100%' }} />
                                        </Form.Item>
                                    </Col>
                                    <Col span={8}>
                                        <Form.Item name="goal" label="Meta / Retiro" rules={[{ required: true, message: 'Requerido' }]}>
                                            <InputNumber style={{ width: '100%' }} />
                                        </Form.Item>
                                    </Col>
                                </Row>
                            </Form>
                        </Modal>

                    </ConfigProvider>'''
if modal_current in content:
    content = content.replace(modal_current, modal_new)
else:
    print('Error: Could not find Modal end to replace.')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Successfully ran replacements!')
