#####Code for GM_Repeater

Rep = nuke.toNode('GM_Repeater1')

Rep.begin()

nuke.toNode('PROXY').knob('knobChanged').setValue("""
m = nuke.thisNode()
kc = nuke.thisKnob()

if kc.name() in ["copies"]:

    for n in nuke.allNodes():
        if "static" not in n['label'].getValue():
            nuke.delete(n)

    
    iRep = m.knob('copies').getValue()
    iRepeats = int(iRep)-1
    bfirstLoop = True
    
    # Main Transform for Copy1
    w = nuke.toNode('Trans_COPY1')
    
    # Last Merge connected to this
    b = nuke.toNode('COPIES1_end')
    
    # Dot would be connected to this and allows toggle between original and modified source 
    s = nuke.toNode('Switch1')
    
    nDot = nuke.nodes.Dot()
    nDot.setInput(0, s)
    
    if (iRepeats+1) >= 2: 
    
        for i in range(iRepeats):
            CTrans = nuke.nodes.Transform(name = "t" + str(i))
            CTrans.knob('translate').setExpression('Trans_COPY1.translate')
            CTrans.knob('rotate').setExpression('Trans_COPY1.rotate')
            CTrans.knob('scale').setExpression('Trans_COPY1.scale')
            CTrans.knob('skewX').setExpression('Trans_COPY1.skewX')
            CTrans.knob('skewY').setExpression('Trans_COPY1.skewY')
            CTrans.knob('skew_order').setExpression('Trans_COPY1.skew_order')
            CTrans.knob('center').setExpression('Trans_COPY1.center')
            CTrans.knob('invert_matrix').setExpression('Trans_COPY1.invert_matrix')
            CTrans.knob('filter').setExpression('Trans_COPY1.filter')
            nMerge = nuke.nodes.Merge2(name = "m" + str(i))
            nMerge.knob('also_merge').setValue('all')
            nMerge.knob('operation').setExpression('Merge_Proxy.operation1')
            nMerge.setInput(1, CTrans)
            
            if bfirstLoop:
                bfirstLoop = False
                CTrans.setInput(0, nDot)
                nMerge.setInput(0, nDot)
            else:
                CTrans.setInput(0, nPrevTrans)
                nMerge.setInput(0, nPrevMerge)
        
            nPrevMerge = nMerge
            nPrevTrans = CTrans
        
        MNum = int(iRepeats) - 1
        
        p = nuke.toNode("m" + str(MNum))
        
        b.setInput(0, p)
    else:
        b.setInput(0, nDot)

""")


Rep.end()
