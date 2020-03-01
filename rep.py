#####Code for GM_Repeater#####


Rep = nuke.toNode('GM_Repeater')

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
    RepMax = int(iRep)
    bfirstLoop = True
    
    # Main Transform for Copy1
    w = nuke.toNode('Trans_COPY1')
    
    # Last Merge connected to this
    b = nuke.toNode('COPIES1_end')
    
    # Dot would be connected to this and allows toggle between original and modified source 
    s = nuke.toNode('Switch1')
    
    nDot = nuke.nodes.Dot()
    nDot.setInput(0, s)

    nMult = nuke.toNode('mu1t2_1')
    
    if (iRepeats+1) >= 2: 
    
        for i in range(iRepeats):
            RepNum = int(i)+1
            RepNum2 = int(i)+2
            nMult.knob('ReMax').setValue( RepMax )
            nMult.knob('value').setExpression('((1/(ReMax-1))*(ReMax-(ReMax-ReNum))) + ( ( 1- ((1/(ReMax-1))*(ReMax-(ReMax-ReNum))) ) * Trans_COPY1_proxy.fadein )')
            CTrans = nuke.nodes.Transform(name = "t" + str(i))
            CTrans.knob('translate').setExpression('Trans_COPY1.translate')
            CTrans.knob('rotate').setExpression('Trans_COPY1.rotate')
            CTrans['scale'].setSingleValue(False)
            CTrans['scale'].setExpression(('Trans_COPY1.scale.w'),0)
            CTrans['scale'].setExpression(('Trans_COPY1.scale.h'),1)
            CTrans.knob('skewX').setExpression('Trans_COPY1.skewX')
            CTrans.knob('skewY').setExpression('Trans_COPY1.skewY')
            CTrans.knob('skew_order').setExpression('Trans_COPY1.skew_order')
            CTrans.knob('center').setExpression('Trans_COPY1.center')
            CTrans.knob('invert_matrix').setExpression('Trans_COPY1.invert_matrix')
            CTrans.knob('filter').setExpression('Trans_COPY1.filter')
            CTrans.knob('motionblur').setExpression('Trans_COPY1.motionblur')
            CTrans.knob('shutter').setExpression('Trans_COPY1.shutter')
            CTrans.knob('shutteroffset').setValue(0)
            CMult1 = nuke.nodes.Multiply(name = "mu1_" + str(i))
            k = nuke.Int_Knob('ReMax', 'ReMax' )
            k2 = nuke.Int_Knob('ReNum', 'ReNum' )
            CMult1.addKnob(k)
            CMult1.addKnob(k2)
            CMult1.knob('ReMax').setValue( RepMax )
            CMult1.knob('ReNum').setValue( RepNum )
            CMult1.knob('value').setExpression('((1/(ReMax-1))*(ReMax-ReNum)) + ( ( 1- ((1/(ReMax-1))*(ReMax-ReNum)) ) * Trans_COPY1_proxy.fadeout )')
            CMult1.setInput(0, CTrans)
            CMult2 = nuke.nodes.Multiply(name = "mu1t2_" + str(RepNum2))
            k = nuke.Int_Knob('ReMax', 'ReMax' )
            k2 = nuke.Int_Knob('ReNum', 'ReNum' )
            CMult2.addKnob(k)
            CMult2.addKnob(k2)
            CMult2.knob('ReMax').setValue( RepMax )
            CMult2.knob('ReNum').setValue( RepNum )
            CMult2.knob('value').setExpression('((1/(ReMax-1))*(ReMax-(ReMax-ReNum))) + ( ( 1- ((1/(ReMax-1))*(ReMax-(ReMax-ReNum))) ) * Trans_COPY1_proxy.fadein )')
            CMult2.setInput(0, CMult1)
            nMerge = nuke.nodes.Merge2(name = "m" + str(i))
            nMerge.knob('also_merge').setValue('all')
            nMerge.knob('operation').setExpression('Merge_Proxy.operation1')
            nMerge.setInput(1, CMult2)
            
            if bfirstLoop:
                bfirstLoop = False
                CTrans.setInput(0, nDot)
                CMult1.setInput(0, CTrans)
                CMult2.setInput(0, CMult1)
                nMerge.setInput(0, nMult)
            else:
                CTrans.setInput(0, nPrevTrans)
                CMult1.setInput(0, CTrans)
                CMult2.setInput(0, CMult1)
                nMerge.setInput(0, nPrevMerge)
 
            nPrevMerge = nMerge
            nPrevTrans = CTrans
            nPrevMult1 = CMult1
            nPrevMult2 = CMult2
        
        MNum = int(iRepeats) - 1
        
        p = nuke.toNode("m" + str(MNum))
        
        b.setInput(0, p)
    else:
        b.setInput(0, nDot)

""")


Rep.end()
